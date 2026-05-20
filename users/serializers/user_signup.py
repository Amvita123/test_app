from rest_framework import serializers
from users.models.users import User
from users.serializers.custom import CustomSerializer

class UserSignUpSerializer(CustomSerializer, serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    profile_pic = serializers.ImageField(required=True)
    gender = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True, max_length=15)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_pic',
                  'gender', 'biograph', 'phone_number', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("password and confirm_password does not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return super().create(validated_data)


class OtpVerificationSerializer(CustomSerializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(min_value=100000, max_value=999999, error_messages={'min_value': 'OTP code must be 6 digits, number',
                                       'max_value': 'OTP code must be 6 digits number',
                                       'invalid': 'Invalid OTP. Please enter a valid 6-digit number.'
                                   })

    def validate(self, attrs):
        email = attrs.get("email").lower()
        user = User.objects.filter(email=email)
        if user.exists() is True:
            attrs['user'] = user.first()
        else:
            raise serializers.ValidationError("email does not exists in database")
        return attrs

class SMSOTPVerificationSerializer(CustomSerializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.IntegerField(min_value=100000, max_value=999999,
                                   error_messages={'min_value': 'OTP code must be 6 digits, number',
                                                   'max_value': 'OTP code must be 6 digits number',
                                                   'invalid': 'Invalid OTP. Please enter a valid 6-digit number.'
                                                   })
    def validate(self, attrs):
        phone_number = attrs.get("phone_number", "")
        user = User.objects.filter(phone_number=phone_number)
        if user.exists() is True:
            attrs['user'] = user.first()
        else:
            raise serializers.ValidationError("phone_number does not exists in database")
        return attrs