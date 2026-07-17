import random
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserRegisterSerializer, UserConfirmSerializer
from .models import Verifications 

class RegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')    
        password = serializer.validated_data.get('password')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )
        
        code = str(random.randint(100000, 999999))
        Verifications.objects.create(user=user, code=code)
        
        return Response(
            data={'user_id': user.id, 'code': code}, 
            status=status.HTTP_201_CREATED
        )

class ConfirmAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=UserConfirmSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        try:
            confirm_code = Verifications.objects.get(code=code)
        except Verifications.DoesNotExist:
            return Response(
                data={'error': 'Invalid or expired code!'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        user = confirm_code.user
        user.is_active = True
        user.save()
        confirm_code.delete()
        
        return Response(
            data={'message': 'User account activated successfully!'}, 
            status=status.HTTP_200_OK
        )

class AuthorizationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(data={'key': token.key})
        except User.DoesNotExist:
            pass
            
        return Response(
            data={'error': 'Invalid credentials or account is not active.'},
            status=status.HTTP_401_UNAUTHORIZED
        )