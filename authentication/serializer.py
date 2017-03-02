from django.contrib.auth.models import User
from rest_framework import serializers


class BasicAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active',)


class FullAccountSerializer(serializers.ModelSerializer):

    username = serializers.CharField(read_only=True, required=False)
    address = serializers.CharField(source='profile.address')
    is_superuser = serializers.BooleanField(read_only=True, required=False)
    is_staff = serializers.BooleanField(read_only=True, required=False)
    is_active = serializers.BooleanField(read_only=True, required=False)
    last_login = serializers.DateTimeField(read_only=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',  'address', 'last_login', 'is_superuser', 'email', 'is_staff', 'is_active', 'date_joined',)