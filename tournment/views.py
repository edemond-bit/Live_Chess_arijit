from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import LeaveSerializer, UserSerializer
from .models import Leave

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all().order_by('name')
    serializer_class = LeaveSerializer