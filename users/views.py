from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .serializers import DetailsSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from .models import Details
from django.forms.models import model_to_dict
import json

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def details_add(request):
    if request.method == 'POST':
        user = Token.objects.get(key=request.auth.key).user
        try:
            if Details.objects.filter(user=user).exists():
                detail = Details.objects.get(user=user)
            else:
                detail = Details()
                detail.user = user
            detail.first_name = request.data['first_name']
            detail.last_name = request.data['last_name']
            detail.age = request.data['age']
            detail.bio = request.data['bio']
            detail.image = request.data['image']
            detail.save()
        except:
            return JsonResponse({"success": "0", "data": [], "message": "Please check user detail entered"})
        serializer = DetailsSerializer(detail)
        return JsonResponse({"success": "1", "data": serializer.data, "message": "User successfully updated"})

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def details_get(request):
    if request.method == 'GET':
        user = Token.objects.get(key=request.auth.key).user
        detail = Details.objects.get(user=user)
        serializer = DetailsSerializer(detail)
        return JsonResponse(serializer.data, safe=False)