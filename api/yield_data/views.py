from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import *
from .models import YieldData
import pickle, json, os
from tensorflow import keras
import numpy as np
from pathlib import Path
import sys, types
from tensorflow.keras.preprocessing.sequence import pad_sequences as tf_pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer as TFTokenizer

# Compatibility shim for legacy pickled objects that reference
# `keras.preprocessing.text.Tokenizer` or `keras.preprocessing.sequence.pad_sequences`.
legacy_preprocessing = types.ModuleType("keras.preprocessing")
legacy_text = types.ModuleType("keras.preprocessing.text")
legacy_sequence = types.ModuleType("keras.preprocessing.sequence")
legacy_text.Tokenizer = TFTokenizer
legacy_sequence.pad_sequences = tf_pad_sequences
sys.modules.setdefault("keras.preprocessing", legacy_preprocessing)
sys.modules.setdefault("keras.preprocessing.text", legacy_text)
sys.modules.setdefault("keras.preprocessing.sequence", legacy_sequence)


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
            serializer = GetYieldSerializer(instance=data, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        try:
            yield_id = request.data.get('id') or request.query_params.get('id')
            if not yield_id:
                return Response("Yield ID is required", status=status.HTTP_400_BAD_REQUEST)
            
            try:
                yield_obj = YieldData.objects.get(id=yield_id)
            except YieldData.DoesNotExist:
                return Response("Yield not found", status=status.HTTP_404_NOT_FOUND)
            
            # Check if user owns the yield or is admin
            if yield_obj.user.id != request.user.id and not request.user.is_staff:
                return Response("You don't have permission to delete this yield", status=status.HTTP_403_FORBIDDEN)
            
            # Delete the image file if it exists
            if yield_obj.image:
                try:
                    yield_obj.image.delete(save=False)
                except Exception:
                    pass  # Continue even if image deletion fails
            
            yield_obj.delete()
            return Response("Yield deleted successfully", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        


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
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        

def chat(inp):
    # Resolve project and data paths robustly
    yield_dir = Path(__file__).resolve().parent
    project_root = Path(__file__).resolve().parents[2]

    model_dir = project_root / 'chat_model'
    intents_path = yield_dir / 'intents.json'
    tokenizer_path = project_root / 'tokenizer.pickle'
    label_encoder_path = project_root / 'label_encoder.pickle'

    if not model_dir.exists():
        return False, "Chat model directory not found."
    if not intents_path.exists():
        return False, "intents.json not found."
    if not tokenizer_path.exists() or not label_encoder_path.exists():
        return False, "Tokenizer or label encoder not found."

    # Load model: support TF SavedModel directory via TFSMLayer for Keras 3
    model = None
    try:
        if model_dir.is_dir():
            tfsml_layer = keras.layers.TFSMLayer(str(model_dir), call_endpoint='serving_default')
            # Wrap layer so we get a `predict`-like callable that returns a tensor/ndarray
            def run_inference(x):
                y = tfsml_layer(x)
                if isinstance(y, dict):
                    y = next(iter(y.values()))
                elif isinstance(y, (list, tuple)):
                    y = y[0]
                return y
            model = run_inference
        else:
            # .keras or .h5 files
            model = keras.models.load_model(str(model_dir))
    except Exception as e:
        return False, f"Failed to load chat model: {str(e)}"
    with open(intents_path) as file:
        data = json.load(file)

    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open(label_encoder_path, 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    max_len = 20
    input_seq = tf_pad_sequences(
        tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len
    )
    # Call either the wrapped TFSMLayer or a Keras model's predict
    try:
        if callable(model) and not hasattr(model, 'predict'):
            result = model(input_seq)
        else:
            result = model.predict(input_seq)
    except Exception as e:
        return False, f"Model inference failed: {str(e)}"

    # Ensure numpy array
    try:
        if hasattr(result, 'numpy'):
            result = result.numpy()
    except Exception:
        pass
    tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]
    for i in data['intents']:
        if i['tag'] == tag:
            response = str(np.random.choice(i['responses']))
            return True, response
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
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):
        try:
            data = ChatBot.objects.filter(user_id=request.user.pk).order_by('id')
            serializer = GetChatBotSerializer(instance=data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("sorry you don't have access", status=status.HTTP_400_BAD_REQUEST)
