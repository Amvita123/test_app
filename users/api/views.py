from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from users.serializers.user_signup import UserSignUpSerializer, OtpVerificationSerializer
from rest_framework import status
from users.serializers.users import UserSerializer
from users.helper.response import success_response, error_response, response_not_found, create_unique_username
from users.services.send_otp_verification import send_otp_to_mail
from users.models import User
from django.core.cache import cache

class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            email = email.lower()
        user_exists = User.objects.filter(email=email).first()
        if user_exists and not user_exists.email_verified:
            send_otp_to_mail(username=f'{user_exists.first_name} {user_exists.last_name}', user_email=user_exists.email.lower(),
                             phone_number=user_exists.phone_number)
            return success_response(
                message="OTP sent to your email. Please verify your account.",
                status_code=status.HTTP_200_OK
            )

        if user_exists and user_exists.email_verified:
            return error_response(message="An account is already registered with this email address. Please proceed to login.",
                                    status_code=status.HTTP_400_BAD_REQUEST)

        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(username=create_unique_username(serializer.validated_data['first_name'],
                                                                   serializer.validated_data['last_name']))
            user.set_password(serializer.validated_data['password'])
            user.is_active = True
            user.save()

            send_otp_to_mail(username=f'{user.first_name} {user.last_name}', user_email=user.email.lower(),
                             phone_number=user.phone_number)

            serialize = UserSerializer(user)
            return success_response(message="User Registered Successfully", data=serialize.data, status_code=status.HTTP_201_CREATED)


class VerifyEmailOtpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            if user.email_verified is True:
                return error_response(
                    message="your email is already verified.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            cache_otp = cache.get(f"otp_{user.email}")

            if cache_otp is None:
                send_otp_to_mail(username=f'{user.first_name} {user.last_name}', user_email=user.email.lower(),
                                 phone_number=user.phone_number
                                 )
                return response_not_found(
                    message="your previous opt was expired. we have resend otp please check your mail.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if str(cache_otp) == str(serializer.validated_data['otp']):
                user.email_verified = True
                user.save()
                return success_response(message="email verified & SMS otp sent successfully", status_code=status.HTTP_200_OK
                                        )
            else:
                return error_response(
                    message="Invalid otp code",
                    status_code=status.HTTP_400_BAD_REQUEST)