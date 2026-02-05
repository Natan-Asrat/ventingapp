from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta
from urllib.parse import urljoin
import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from django.conf import settings

def get_readable_time_since(time_to_compare):
    """
    Returns a human-readable string:
    - 'X ago' if in the past
    - 'X left' if in the future
    """
    delta = timezone.now() - time_to_compare

    if delta.total_seconds() >= 0:
        # past
        if delta < timedelta(minutes=1):
            return "just now"
        elif delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta < timedelta(days=7):
            days = delta.days
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            return f"{timesince(time_to_compare)} ago"
    else:
        # future
        delta = -delta  # make positive
        if delta < timedelta(minutes=1):
            return "less than a minute left"
        elif delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} left"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} left"
        elif delta < timedelta(days=7):
            days = delta.days
            return f"{days} day{'s' if days != 1 else ''} left"
        else:
            return f"{timesince(timezone.now(), time_to_compare)} left"


def rsa_signer(message):
    """
    Helper function to sign the CloudFront policy using your private key.
    """
    # You should store the path to your .pem file in your .env / settings
    with open(settings.CLOUDFRONT_PRIVATE_KEY_PATH, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

def generate_cloudfront_signed_url(key):
    if not settings.CLOUDFRONT_REQUIRES_KEY:
        return urljoin(settings.BACKEND_URL, key.url)
    try:
        url_base = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}"
        
        # Set the expiration time (e.g., 5 minutes from now)

        expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=2)
        
        # Initialize the CloudFront Signer
        cf_signer = CloudFrontSigner(settings.CLOUDFRONT_KEY_PAIR_ID, rsa_signer)
        
        # Generate the signed URL
        signed_url = cf_signer.generate_presigned_url(
            url_base, date_less_than=expire_date
        )
        return signed_url
    except Exception as e:
        print(f"Error generating CloudFront URL: {e}")
        return None