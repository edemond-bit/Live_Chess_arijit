from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse

from tournment.models import Leave
from users.models import *
from django.contrib.auth.models import User

from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_auth.app_settings import LoginSerializer, TokenSerializer, create_token
from rest_auth.registration.app_settings import RegisterSerializer, register_permission_classes
from rest_auth.models import TokenModel
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from tournment.serializers import DashboardSerializer
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    dataset = dict()
    leaves = Leave.objects.all_approved_leaves()
    employee = Employee.objects.all()
    dataset['leave_list'] = leaves
    dataset['employee'] = employee

    return render(request, '_layout.html', dataset)

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework
    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        return response

    def post(self, request, *args, **kwargs):
        response = None
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        if (self.serializer.is_valid()):
            self.serializer.is_valid(raise_exception=True)
            self.login()
            data = {"success": "1", "message": "Successfully Login"}
            response = self.get_response()
            response.data.update(data)
        else:
            data = {"success": "0", "user": [], "message": "Check user name or password"}
            response = JsonResponse(data, safe=False)
        return response

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        # if allauth_settings.EMAIL_VERIFICATION == \
        #         allauth_settings.EmailVerificationMethod.MANDATORY:
        #     return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)

        # complete_signup(self.request._request, user,
        #                 allauth_settings.EMAIL_VERIFICATION,
        #                 None)
        return user

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def DashboardViewSet(request):
    if request.method == 'GET':
        leave = Leave.objects.filter(user=request.user, is_approved=True)
        serializer = DashboardSerializer(leave, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def HomeViewSet(request):
    if request.method == 'GET':
        leave = Leave.objects.all_approved_leaves()
        serializer = HomeSerializer(leave, many=True)
        return JsonResponse(serializer.data, safe=False)


def file_transfer(request):
    # import shutil
    # import os
    # source_path = r"\\192.168.42.32\pn\move\move1.pgn"
    # print(os.listdir(r"\\192.168.225.36\\"))
    # source_path = r"\\192.168.225.36\moves\1\move2.pgn"
    # dest_path = r"E:\\"
    # shutil.copy(source_path, dest_path)
    # import subprocess
    # subprocess.run(["scp", "ubuntu@54.183.117.48:/home/ubuntu/Chess/media/documents/move7.pgn", "E:\\"])

    import os
    import paramiko
    from io import StringIO
    f = os.path.expanduser('~\Downloads\private_key1.ppk')
    # with open(f, 'r') as file:
    #     data = file.read().replace('\n', '')
    # private_key = StringIO(data)
    k = paramiko.RSAKey.from_private_key_file(f)
    # file = paramiko.util.load_host_keys(os.path.expanduser('~\Downloads\Chess_Phythonn.ppk'))

    host = '54.183.117.48'
    # host = '192.168.42.32'
    port = 22
    username = 'ubuntu'

    remote_path = r'/home/ubuntu/Chess/media/documents/move7.pgn'
    # remote_path = r'/home/ubuntu/Chess/media/documents/move8.pgn'
    local_path = r'E:\Live_Chess_arijit-main\media\server_data\abc.pgn'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, port=port, password="", key_filename=k)
    sftp = ssh.open_sftp()
    sftp.get(local_path, remote_path)

    sftp.close()
    ssh.close()

    return JsonResponse({"success": 1})
