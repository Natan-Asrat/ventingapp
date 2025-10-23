import pyotp
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta

def send_email_otp(user, subject="Your Verification Code"):
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        user.save()
    
    totp = pyotp.TOTP(user.otp_secret, interval=300)  # 5-minute OTP
    otp = totp.now()
    
    send_mail(
        subject=subject,
        message=f'Your OTP code is: {otp}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def verify_email_otp(user, submitted_otp, interval=300):
    totp = pyotp.TOTP(user.otp_secret, interval=interval)
    
    if totp.verify(submitted_otp, valid_window=1):
        user.email_verified = True
        user.save()
        return True
    return False