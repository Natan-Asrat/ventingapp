from polar_sdk.models import SubscriptionStatus
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Transaction
from .serializers import TransactionsSimpleSerializer, SubscriptionsSimpleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .polar import polar
from django.conf import settings
from .models import PaymentMethods
from polar_sdk.webhooks import validate_event
from .models import Subscription, Customer
from server.utils import get_readable_time_since
from django.utils import timezone

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
            transaction_id=checkout.id
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
    