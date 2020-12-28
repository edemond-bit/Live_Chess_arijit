from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Leave

# profile, membership, home, dashboard

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email']

class LeaveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Leave
        fields = fields = ['id', 'name','desc','location','type','country','laws','startdate','starttime',
                           'enddate','endtime','rounds','user','status','is_approved',
                           'created', 'updated',]
        read_only_fields = ('timezone',)