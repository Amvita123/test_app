from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.SignUpAPIView.as_view(), name='sign_up'),
    path('verify-email-otp/', views.VerifyEmailOtpAPIView.as_view(), name='verify_email_otp'),
]