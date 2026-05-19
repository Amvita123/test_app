from rest_framework import serializers
from users.models.users import User

class UserSignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    profile_pic = serializers.ImageField(required=True)
    gender = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_pic',
                  'gender', 'biograph', 'phone_number', 'password']