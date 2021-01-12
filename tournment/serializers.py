from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Leave
from timezone_field.rest_framework import TimeZoneSerializerField
from rest_auth.models import TokenModel
from users.serializers import UserSerializer

# profile, membership, home, dashboard

class LogInSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password']

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TokenModel
        fields = ('key', 'user')

class LeaveSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()

    class Meta:
        model = Leave
        fields = ['id', 'name','desc','location','type','country','laws','startdate','starttime',
                           'enddate','endtime','rounds','user','status','is_approved', 'timezone',
                           'created', 'updated',]

class DashboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leave
        fields = ['id', 'name', 'desc']

class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leave
        fields = ['id', 'name', 'desc']