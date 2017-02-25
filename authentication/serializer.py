from django.contrib.auth.models import User
from rest_framework import serializers


class BasicAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'is_active',)


class FullAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'last_login', 'is_superuser', 'email', 'is_staff', 'is_active', 'date_joined',)