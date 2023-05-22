from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class IrisSerializer(serializers.Serializer):
    blade_radius = serializers.FloatField()
    pinned_radius = serializers.FloatField()
    min_angle = serializers.FloatField()
    max_angle = serializers.FloatField()
    bc = serializers.FloatField()
