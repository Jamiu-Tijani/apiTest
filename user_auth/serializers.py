from rest_framework import serializers
from . import models

class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.userData
        fields = ['username','password','email']

class userdataSerializer(serializers.ModelSerializer):
    new_username = serializers.CharField(
        max_length=68, write_only=True)
    class Meta:
        model = models.userData
        fields = ['username','password','new_username']

    