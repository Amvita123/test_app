from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from users.serializers.user_signup import UserSignUpSerializer
from rest_framework import status
from rest_framework.response import Response
from users.serializers.users import UserSerializer
from users.helper.response import success_response, error_response, create_unique_username
from users.services.send_otp_verification import send_otp_to_mail
from users.models import User

class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
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

        try:
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

        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)