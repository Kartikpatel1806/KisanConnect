from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import *
from .models import *
from .face_kyc import capture
import os
from pathlib import Path


def passwd_lookup(value):
    min_length = 8
    errors = []
    is_valid = []
    if len(value) < min_length:
        errors.append(('Password must be at least {0} characters long.').format(min_length))
        is_valid.append(True)
    if not any(char.isdigit() for char in value):
        errors.append('Password must contain at least 1 digit.')
        is_valid.append(True)
    if not any(char.isalpha() for char in value):
        errors.append('Password must contain at least 1 letter.')
        is_valid.append(True)

    if any(is_valid):
        return True, errors
    return False, None

class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request,format=None):
        try:
            email = request.data.get('email', '').strip()
            name = request.data.get('name', '').strip()
            role = request.data['role']['key']
            passwd = request.data.get('password', '').strip()
                
            if len(email) <= 0:
                return Response('Email should not be empty.', status=status.HTTP_400_BAD_REQUEST)
            if len(passwd) <= 0:
                return Response('Password should not be empty.', status=status.HTTP_400_BAD_REQUEST)
            if UserModel.objects.filter(email = email).exists():
                return Response(f'{email} already exist, please try with different email address.', status=status.HTTP_400_BAD_REQUEST)
            
            has_error, errors = passwd_lookup(passwd)
            if has_error:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            user_data = {}
            user_data['email'] = email
            user_data['name'] = name
            user_data['role'] = role
            user_data['password']  = passwd
                
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()                
                return Response((user_serializer.data), status=status.HTTP_201_CREATED)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        

    def get(self,request,format=None):
        try:
            user = UserModel.objects.filter(id=request.auth.user.pk).order_by('id')
            serializer = UserSerializer(instance=user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        

    def put(self,request,format=None):
        try:
            msg = ""
            request_data = request.data
            user_id = request_data['id']
            if 'file' not in request_data.keys():
                return Response("Invalid Filename", status=status.HTTP_400_BAD_REQUEST)
            _file_ = request_data['file']
            # Resolve Downloads directory of the current server user dynamically
            path = str(Path.home() / 'Downloads')
            if not os.path.isdir(path):
                return Response("Downloads folder not found on server.", status=status.HTTP_400_BAD_REQUEST)
            text_files = [f for f in os.listdir(path) if f.endswith('.webm')]
            if _file_ in text_files:
                text_files = os.path.join(path, _file_)
                print(text_files)
                is_valid, msg = capture(text_files)
                if is_valid:
                    user = UserModel.objects.get(id=user_id)
                    user.is_kyc = True
                    user.save()
                    return Response("KYC has been done!", status=status.HTTP_200_OK)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self,request,format=None):
        try:
            user = UserModel.objects.get(id=request.auth.user.pk)
            if not user.is_admin:
                return Response("Only Admin have access this", status=status.HTTP_400_BAD_REQUEST)
            request_data = request.data
            user_id = request_data['id']
            user = UserModel.objects.get(id=user_id)
            user.delete()
            return Response("Successfully deleted!", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)