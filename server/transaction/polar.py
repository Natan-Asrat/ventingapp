from polar_sdk import Polar
from django.conf import settings

polar = Polar(
    access_token=settings.POLAR_ACCESS_TOKEN,
    server=settings.POLAR_SERVER
)