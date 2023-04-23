from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import *


class YieldView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,format=None):
        try:
            request_data = request.data
            description = None if not request_data['description'] else request_data['description']
            if 'image' in request.FILES.keys():
                image = request.FILES['image']
                
                data = {}
                data['description'] = description
                data['image'] = image
                data['user'] = request.user.pk
                serializer = YieldSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):
        try:
            data = YieldData.objects.filter().order_by('id')
            serializer = GetYieldSerializer(instance=data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        


class BotView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,format=None):
        try:
            request_data = request.data
            query = request_data['query'].strip()
            yield_id = request_data['yield_id']
            if len(query) <= 0:
                return Response("query field cannot be empty.", status=status.HTTP_400_BAD_REQUEST)  
            data = {}
            data['query'] = query
            data['yield_data'] = yield_id
            data['user'] = request.user.pk
            serializer = BotSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):
        try:
            id = request.GET.get('id')
            data = Bot.objects.filter(yield_data=id).order_by('id')
            serializer = GetBotSerializer(instance=data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)