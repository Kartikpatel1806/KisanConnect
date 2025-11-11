from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from pathlib import Path



def recommendation(n_params,p_params,k_params,t_params,h_params,ph_params,r_params):
    try:
        # Resolve CSV relative to this file to avoid CWD issues
        csv_path = Path(__file__).resolve().parent / 'Crop_recommendation.csv'
        dataset = pd.read_csv(str(csv_path))
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, -1].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
        classifier.fit(X_train, y_train)
        user_input = np.array([[n_params,p_params,k_params,t_params,h_params,ph_params,r_params]])
        predictions = classifier.predict(user_input)
        print(str(predictions[0]))
        return True, str(predictions[0])
    except Exception as e:
        return False, str(e)


class CropView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,format=None):
        try:
            request_data = request.data
            nitrogen = int(request_data['nitrogen'])
            phosphorus = int(request_data['phosphorus'])
            potassium = int(request_data['potassium'])
            temperature = float(request_data['temperature'])
            humidity = float(request_data['humidity'])
            ph = float(request_data['ph'])
            rainfall = float(request_data['rainfall'])

            is_valid, result = recommendation(nitrogen,phosphorus,potassium,temperature,humidity,ph,rainfall)
            if is_valid:
                data = {}
                data['nitrogen'] = nitrogen
                data['phosphorus'] = phosphorus
                data['potassium'] = potassium
                data['temperature'] = temperature
                data['humidity'] = humidity
                data['ph'] = ph
                data['rainfall'] = rainfall
                data['user'] = request.user.pk
                data['result'] = result
                serializer = CropSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):
        try:
            data = CropData.objects.filter().order_by('id')
            serializer = GetCropSerializer(instance=data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)