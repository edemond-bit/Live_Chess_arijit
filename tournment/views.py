from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import LeaveSerializer
from .models import Leave
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def TournamentViewSet(request):
    if request.method == 'GET':
        leave = Leave.objects.filter(user=request.user)
        serializer = LeaveSerializer(leave, many=True)
        return JsonResponse(serializer.data, safe=False)
# class LeaveViewSet(viewsets.ModelViewSet):
#     queryset = Leave.objects.all().order_by('name')
#     serializer_class = LeaveSerializer

# def tournament(request):
#     content = {"message": "Welcome to the BookStore!"}
#     return JsonResponse(content)