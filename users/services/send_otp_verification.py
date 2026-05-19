from  django.template.loader import render_to_string
import random
from django.core.cache import cache
from datetime import datetime
from users.task import auth_mail_send

def send_otp_to_mail(username, user_email, phone_number):
    otp = random.randint(100000, 999999)
    html_message = render_to_string('mail/otp_verification.html', {
        'username': username.title(),
        'otp': otp,
        "year": str(datetime.now().year)
    })
    cache.set(f"otp_{user_email}", otp, 60*10)
    subject = 'OTP for Verification'
    auth_mail_send.delay(subject, html_message, user_email)