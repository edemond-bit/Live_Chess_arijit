from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Details

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class DetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Details
        fields = '__all__'