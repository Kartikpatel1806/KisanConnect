from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import *
import pickle, json, os
from tensorflow import keras
import numpy as np


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
        


class QueryView(APIView):
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
            serializer = QuerySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):
        try:
            id = request.GET.get('id')
            data = Query.objects.filter(yield_data=id).order_by('id')
            serializer = GetQuerySerializer(instance=data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        

def chat(inp):
    model = keras.models.load_model('chat_model')
    dir = os.getcwd()
    dir = dir + "/api/yield_data/intents.json"
    print(dir)
    with open(dir) as file:
        data = json.load(file)

    response = ""
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
    max_len = 20
    
    while True:
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        for i in data['intents']:
            if i['tag'] == tag:
                response = str(np.random.choice(i['responses']))
        if response:
            return True, response
        else:
            return False, None

class ChatBotView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request,format=None):
        try:
            request_data = request.data
            question = request_data['question'].strip().lower()
            if len(question) <= 0:
                return Response("Question can not be empty", status=status.HTTP_400_BAD_REQUEST)
            is_valid, answer = chat(question)
            if not is_valid:
                return Response("I didn't get your query!", status=status.HTTP_400_BAD_REQUEST)
            qna_data = {}
            qna_data['query'] = question
            qna_data['answer'] = answer
            qna_data['user'] = request.user.pk
            qna_data = ChatBotSerializer(data=qna_data)
            if qna_data.is_valid():
                qna_data.save()
                return Response(qna_data.data, status=status.HTTP_201_CREATED)
            return Response(qna_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):
        try:
            data = ChatBot.objects.filter(user_id=request.user.pk).order_by('id')
            serializer = GetChatBotSerializer(instance=data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("sorry you don't have access", status=status.HTTP_400_BAD_REQUEST)
