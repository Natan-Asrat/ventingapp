from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from .models import Transaction
from django.conf import settings
from django.utils import timezone
def add_params(url, params):
    url_parts = urlparse(url)
    query = parse_qs(url_parts.query)

    # Merge new params
    query.update(params)

    new_query = urlencode(query, doseq=True)

    return urlunparse((
        url_parts.scheme,
        url_parts.netloc,
        url_parts.path,
        url_parts.params,
        new_query,
        url_parts.fragment
    ))

def add_connects(connects, user):
    if hasattr(user, "connects"):
        print("user connects before", user.connects)
        user.connects = (user.connects or 0) + connects
        user.save(update_fields=["connects"])
        print("updated user connects to", user.connects)

def add_monthly_free_connects(user):
    transaction = Transaction.objects.create(
        user=user,
        method="Bonus",
        product_name="Free Monthly Connects",
        is_payment_required=False,
        connects=settings.MONTHLY_FREE_CONNECTS,
        currency="USD",
        status="approved",
    )
    transaction.approved = True
    transaction.save()

    user.last_month_free_connects_date = timezone.now()
    user.save()


def add_signup_free_connects(user):
    transaction = Transaction.objects.create(
        user=user,
        method="Bonus",
        product_name="Free Signup Connects",
        is_payment_required=False,
        connects=settings.SIGNUP_FREE_CONNECTS,
        currency="USD",
        status="approved",
    )
    transaction.approved = True
    transaction.save()

    user.last_month_free_connects_date = timezone.now()
    user.save()