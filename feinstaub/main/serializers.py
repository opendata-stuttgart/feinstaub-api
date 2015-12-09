from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("notification_type", "pushover_clientkey", "notifymyandroid_apikey")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')
