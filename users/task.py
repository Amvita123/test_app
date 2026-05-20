from celery import shared_task
from django.utils.html import strip_tags
from django.conf import settings
from  django.core.mail import send_mail
from twilio.rest import Client

@shared_task
def auth_mail_send(subject, html_message, user_email):
    plain_message = strip_tags(html_message)
    try:
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user_email], html_message=html_message)
        return "Mail sent successfully"

    except Exception as e:
        return f"error to sending email: {e}"

@shared_task
def send_sms(phone_number, sms_body):
    print("hjh")
    if not phone_number:
        return "phone number not provided"

    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=settings.TWILIO_PHONE_NUMBER,
            body=sms_body,
            to=phone_number
        )
    except Exception as e:
        print(str(e))

    return "send twilio sms"