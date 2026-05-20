from rest_framework import serializers
from users.serializers.custom import CustomSerializer
from users.models import User

class UserSerializer(CustomSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'profile_pic', 'gender', 'biograph', 'phone_number',
                  'email_verified', 'sms_verified']