from polar_sdk.models import SubscriptionStatus
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .utils import add_monthly_free_connects, safe_usd_equivalent
from .models import (
    ManualTransactionStatus, 
    Transaction,
    ManualPaymentDecision,
    PaymentMethods, 
    ManualPaymentOption,
    Subscription, 
    Customer
)
from decimal import Decimal
from .serializers import (
    TransactionsSimpleSerializer, 
    SubscriptionsSimpleSerializer,
    ManualPaymentOptionSerializer
)
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .polar import polar
from django.conf import settings
from polar_sdk.webhooks import validate_event
from server.utils import get_readable_time_since
from django.utils import timezone
from datetime import timedelta
from django.db import transaction as db_transaction, OperationalError

from rest_framework.permissions import IsAdminUser
from account.pagination import CustomPagination

# Create your views here.
def get_amount_by_product_id(product_id):
    for option in settings.POLAR_ORDER_OPTIONS.values():
        if option["product_id"] == product_id:
            return option["connects"]
    return None

def get_key_by_product_id(product_id):
    for key, value in settings.POLAR_ORDER_OPTIONS.items():
        if value['product_id'] == product_id:
            return key
    return None  # if not found

def get_polar_amount_in_dollar(amount):
    return amount / 100

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSimpleSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        product = request.data.get('product')
        order_option = settings.POLAR_ORDER_OPTIONS.get(product)
        current_url = request.data.get('current_url')
        if not order_option:
            return Response({"error": "Invalid product"}, status=400)
        checkout = polar.checkouts.create(request={
            "products": [order_option['product_id']],
            "success_url": current_url
        })
        Transaction.objects.create(
            user=request.user,
            method=PaymentMethods.POLAR,
            transaction_id=checkout.id,
            requires_approval=False
        )
        return Response({"checkout_url": checkout.url})
    
    @action(detail=False, methods=['get'])
    def connect_options(self, request):
        user = request.user
        result = {}

        for code, option in settings.POLAR_ORDER_OPTIONS.items():
            # Copy option but exclude product_id
            sanitized_option = {k: v for k, v in option.items() if k != "product_id"}

            # If it's a subscription product, check if user is subscribed
            if option.get("is_sub"):
                subscribed = Subscription.objects.filter(
                    user=user,
                    is_active=True,
                    product_code_internal=code
                ).exists()
                sanitized_option["subscribed"] = subscribed

            result[code] = sanitized_option

        return Response(result)

    @action(detail=False, methods=['get'])
    def manual_payment_options(self, request):
        options = ManualPaymentOption.objects.filter(active=True)
        serializer = ManualPaymentOptionSerializer(options, many=True)
        return Response(serializer.data)
    
        
    @action(detail=False, methods=['get'])
    def recent_success(self, request):
        # Get the most recent successful transaction for the current user
        transaction = Transaction.objects.filter(
            user=request.user,
            celebrated=False,
            approved=True,
            connects__isnull=False
        ).order_by('-created_at').first()
        
        if not transaction:
            return Response({})
            
        return Response({
            'connects': transaction.connects,
            'subscription_id': transaction.subscription_id,
            'formatted_created_at': get_readable_time_since(transaction.created_at)
        })

    @action(detail=False, methods=['post'])
    def celebrated(self, request):
        transactions_updated = Transaction.objects.filter(
            user=request.user,
            celebrated=False,
            approved=True,
            connects__isnull=False
        ).update(
            celebrated=True
        )
        return Response({"updated": transactions_updated}, status=200)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def order_paid(self, request):
        event = validate_event(
            body=request.body,
            headers=request.headers,
            secret=settings.POLAR_ORDER_PAID_WEBHOOK_SECRET,
        )
        if not event:
            return Response({"error": "Invalid event"}, status=400)
        print("event", event.model_dump_json())
        product_id = event.data.product_id
        product_code_internal = get_key_by_product_id(product_id)
        print("prod code", product_code_internal)
        connects = get_amount_by_product_id(event.data.product_id)
        if not connects:
            return Response({"error": "Invalid product"}, status=400)
        transaction = Transaction.objects.get(transaction_id=event.data.checkout_id)
        ## finance
        transaction.subtotal_amount = get_polar_amount_in_dollar(event.data.subtotal_amount)
        transaction.total_amount = get_polar_amount_in_dollar(event.data.total_amount)
        transaction.net_amount = get_polar_amount_in_dollar(event.data.net_amount)
        transaction.tax_amount = get_polar_amount_in_dollar(event.data.tax_amount)
        transaction.discount_amount = get_polar_amount_in_dollar(event.data.discount_amount)
        transaction.refunded_amount = get_polar_amount_in_dollar(event.data.refunded_amount)
        transaction.refunded_tax_amount = get_polar_amount_in_dollar(event.data.refunded_tax_amount)

        transaction.usd_equivalent = transaction.net_amount

        transaction.discount_id = event.data.discount_id
        transaction.connects = connects
        transaction.currency = event.data.currency
        transaction.invoice_number = event.data.invoice_number
        transaction.is_invoice_generated = event.data.is_invoice_generated

        ## product
        transaction.product_id = event.data.product.id
        transaction.product_name = event.data.product.name
        transaction.product_description = event.data.product.description

        transaction.status = event.data.status
        

        transaction.approved = event.data.paid
        transaction.requires_approval = not event.data.paid
        customer_obj = None
        if event.data.customer_id:
            try:
                customer_obj = Customer.objects.get(customer_id=event.data.customer_id)
            except Customer.DoesNotExist:
                customer_obj = Customer.objects.create(
                    user=transaction.user,
                    customer_id=event.data.customer_id,
                    email=event.data.customer.email,
                    name=event.data.customer.name,
                    tax_id=event.data.customer.tax_id,
                    country=event.data.customer.billing_address.country
                )
        subscription_obj = None
        if event.data.subscription_id:
            try:
                subscription_obj = Subscription.objects.get(subscription_id=event.data.subscription_id)
            except Subscription.DoesNotExist:
                subscription_obj = Subscription.objects.create(
                    user=transaction.user,
                    customer=customer_obj,
                    subscription_id=event.data.subscription_id,
                    amount=get_polar_amount_in_dollar(event.data.subscription.amount),
                    current_period_start=event.data.subscription.current_period_start,
                    current_period_end=event.data.subscription.current_period_end,
                    trial_start=event.data.subscription.trial_start,
                    trial_end=event.data.subscription.trial_end,
                    product_id =event.data.product.id,
                    product_code_internal = product_code_internal,
                    product_name = event.data.product.name,
                    recurring_interval_count = event.data.subscription.recurring_interval_count,
                    recurring_interval = event.data.subscription.recurring_interval,
                    is_active=event.data.subscription.status == SubscriptionStatus.ACTIVE
                )
        
        transaction.customer = customer_obj
        transaction.subscription = subscription_obj
        transaction.billing_name = event.data.billing_name
        transaction.product_code_internal = product_code_internal
        transaction.reason = event.data.billing_reason
        transaction.save()
        return Response(status=200)
    
    @action(detail=False, methods=['get'])
    def my_subscriptions(self, request):
        subscriptions = Subscription.objects.filter(user=request.user).order_by('-is_active', '-created_at', 'current_period_end')
        now = timezone.now()

        for sub in subscriptions:
            sub_id = sub.subscription_id
            if sub.current_period_end < now and sub.is_active:
                print("expired sub", sub_id)
                res = polar.subscriptions.get(id=sub_id)
                print("sub data", res.model_dump_json())
                sub.current_period_end = res.current_period_end
                sub.current_period_start = res.current_period_start
                sub.trial_start = res.trial_start
                sub.trial_end = res.trial_end
                sub.is_active = res.status == SubscriptionStatus.ACTIVE
                sub.save()

        serializer = SubscriptionsSimpleSerializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def pending_transactions(self, request):
        transactions = Transaction.objects.filter(requires_approval=True, approved=False, rejected=False).order_by('-created_at')
        serializer = TransactionsSimpleSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve_transaction(self, request, pk=None):
        transaction = self.get_object()
        transaction.approved = True
        transaction.rejected = False
        transaction.status = ManualTransactionStatus.APPROVED
        transaction.status = "Admin Approved Valid Manual Payment"
        transaction.save()

        ManualPaymentDecision.objects.create(
            transaction=transaction,
            decision_maker=request.user,
            approved=True,
            rejected=False,
            reason="Admin Approved Valid Manual Payment"
        )

        return Response(status=200)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject_transaction(self, request, pk=None):
        transaction = self.get_object()
        reason = request.data.get('reason')
        transaction.reason = reason
        transaction.status = ManualTransactionStatus.REJECTED
        transaction.approved = False
        transaction.rejected = True
        transaction.save()

        ManualPaymentDecision.objects.create(
            transaction=transaction,
            decision_maker=request.user,
            approved=False,
            rejected=True,
            reason=reason
        )

        return Response(status=200)

    @action(detail=False, methods=['get'])
    def my_transactions(self, request):
        qs = Transaction.objects.filter(user=request.user).order_by('-created_at')
        paginated_queryset = self.paginate_queryset(qs)
        if paginated_queryset is not None:
            serializer = TransactionsSimpleSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TransactionsSimpleSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def check_monthly_free_connects(self, request):
        now = timezone.now()
        last_free_connect_date = request.user.last_month_free_connects_date

        try:
            with db_transaction.atomic():
                # Lock the user row to prevent race conditions
                user = type(request.user).objects.select_for_update(nowait=True).get(pk=request.user.pk)
                last_free_connect_date = user.last_month_free_connects_date

                if not last_free_connect_date or (now - last_free_connect_date) >= timedelta(days=30):
                    add_monthly_free_connects(user)
                    return Response({"message": "It's time!"})

                return Response({"message": "Not yet..."})

        except OperationalError:
            # This triggers if the row is locked by another transaction
            return Response({"message": "Please try again shortly, another process is updating your free connects."}, status=200)
    

class ManualPaymentViewSet(viewsets.ModelViewSet):
    queryset = ManualPaymentOption.objects.filter(active=True)
    serializer_class = ManualPaymentOptionSerializer

    @action(detail=True, methods=['post'])
    def submit_payment(self, request, pk=None):
        amount_transferred = Decimal(request.data.get('amount_transferred'))
        connects_to_buy = Decimal(request.data.get('connects_to_buy'))        
        manual_payment_option = self.get_object()
        print("connects to buy", connects_to_buy)
        print("amount transferred", amount_transferred)
        screenshot = request.FILES.get('screenshot')
        if not screenshot:
            return Response({"error": "Screenshot is required"}, status=400)
        exchange_rate = manual_payment_option.exchange_rate
        print("exchange rate", exchange_rate)
        print("what should be ", int(exchange_rate * amount_transferred))
        print("what is ", int(connects_to_buy))
        if int(exchange_rate * connects_to_buy) != int( amount_transferred):
            return Response({"error": "Amount transferred is not equal to connects to buy"}, status=400)
        currency = manual_payment_option.currency
        method = manual_payment_option.method

        usd_equivalent = safe_usd_equivalent(amount_transferred, exchange_rate)

        transaction = Transaction.objects.create(
            user=request.user,
            currency=currency,
            method=method,

            product_name="Connects - Manual Payment",

            subtotal_amount=amount_transferred,
            total_amount=amount_transferred,
            net_amount=amount_transferred,

            usd_equivalent=usd_equivalent,

            requires_approval=True,
            approved=False,
            screenshot=screenshot,
            
            connects=connects_to_buy,
            manual_payment_option=manual_payment_option,
            status="pending"
        )
    
        return Response(status=200)