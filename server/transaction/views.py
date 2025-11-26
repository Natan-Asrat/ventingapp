from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Transaction
from .serializers import TransactionsSimpleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .polar import polar
from django.conf import settings
from .models import PaymentMethods
from polar_sdk.webhooks import validate_event
from .models import Subscription, Customer
# Create your views here.
def get_amount_by_product_id(product_id):
    for option in settings.POLAR_ORDER_OPTIONS.values():
        if option["product_id"] == product_id:
            return option["price"]
    return None

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSimpleSerializer

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        product = request.data.get('product')
        order_option = settings.POLAR_ORDER_OPTIONS.get(product)
        if not order_option:
            return Response({"error": "Invalid product"}, status=400)
        checkout = polar.checkouts.create(request={
            "products": [order_option['product_id']],
        })
        Transaction.objects.create(
            user=request.user,
            method=PaymentMethods.POLAR,
            transaction_id=checkout.id
        )
        return Response({"checkout": checkout.url})
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def order_paid(self, request):
        event = validate_event(
            body=request.body,
            headers=request.headers,
            secret=settings.POLAR_ORDER_PAID_WEBHOOK_SECRET,
        )
        if not event:
            return Response({"error": "Invalid event"}, status=400)
        connects = get_amount_by_product_id(event.data.product_id)
        if not connects:
            return Response({"error": "Invalid product"}, status=400)
        transaction = Transaction.objects.get(transaction_id=event.data.checkout_id)
        ## finance
        transaction.subtotal_amount = event.data.subtotal_amount
        transaction.total_amount = event.data.total_amount
        transaction.net_amount = event.data.net_amount
        transaction.tax_amount = event.data.tax_amount
        transaction.discount_amount = event.data.discount_amount
        transaction.refunded_amount = event.data.refunded_amount
        transaction.refunded_tax_amount = event.data.refunded_tax_amount


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
                    subscription_id=event.data.subscription_id
                )
        
        transaction.customer = customer_obj
        transaction.subscription = subscription_obj
        transaction.billing_name = event.data.billing_name
        transaction.save()
        return Response(status=200)
    
    