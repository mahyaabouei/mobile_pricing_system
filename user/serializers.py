from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User , Otp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'


class OtpInputSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)

class LoginInputSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)


class UserInputSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, allow_blank=True)
    otp = serializers.CharField(required=True, allow_blank=True)
    uniqidentifier = serializers.CharField(required=True, allow_blank=True)
    username = serializers.CharField(required=True, allow_blank=True)
    first_name = serializers.CharField(required=True, allow_blank=True)
    last_name = serializers.CharField(required=True, allow_blank=True)
    email = serializers.EmailField(required=True, allow_blank=True)
    address = serializers.CharField(required=True, allow_blank=True)
    city = serializers.CharField(required=True, allow_blank=True)
    company = serializers.CharField(required=True, allow_blank=True)
    sheba_number = serializers.CharField(required=True, allow_blank=True)
    card_number = serializers.CharField(required=True, allow_blank=True)
    account_number = serializers.CharField(required=True, allow_blank=True)
    account_bank = serializers.CharField(required=True, allow_blank=True)
