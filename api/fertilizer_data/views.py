from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import *
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
from pathlib import Path



def recommendation(t_params,h_params,sm_params,soil_type,crop_type,n_params,p_params,k_params):
    try:
        csv_path = Path(__file__).resolve().parent / 'fertilizer_recommendation.csv'
        data = pd.read_csv(str(csv_path))
        le_soil = LabelEncoder()
        data['Soil Type'] = le_soil.fit_transform(data['Soil Type'])
        le_crop = LabelEncoder()
        data['Crop Type'] = le_crop.fit_transform(data['Crop Type'])
        X = data.iloc[:, :8]
        y = data.iloc[:, -1]
        dtc = DecisionTreeClassifier(random_state=0)
        dtc.fit(X, y)
        soil_type = le_soil.transform([soil_type])[0]
        crop_type = le_crop.transform([crop_type])[0]
        user_input = [[t_params,h_params,sm_params,soil_type,crop_type,n_params,p_params,k_params]]

        fertilizer_name = dtc.predict(user_input)
        print(str(fertilizer_name[0]))
        return True, str(fertilizer_name[0])
    except Exception as e:
        return False, str(e)


class FertilizerView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,format=None):
        try:
            request_data = request.data
            nitrogen = int(request_data['nitrogen'])
            phosphorus = int(request_data['phosphorus'])
            potassium = int(request_data['potassium'])
            temperature = int(request_data['temperature'])
            humidity = int(request_data['humidity'])
            soil_moisture = int(request_data['soil_moisture'])
            soil_type = request_data['soil_type']
            crop_type = request_data['crop_type']

            is_valid, result = recommendation(temperature,humidity,soil_moisture,soil_type,crop_type,nitrogen,phosphorus,potassium)
            if is_valid:
                data = {}
                data['nitrogen'] = nitrogen
                data['phosphorus'] = phosphorus
                data['potassium'] = potassium
                data['temperature'] = temperature
                data['humidity'] = humidity
                data['soil_moisture'] = soil_moisture
                data['soil_type'] = soil_type
                data['crop_type'] = crop_type
                data['user'] = request.user.pk
                data['result'] = result
                serializer = FertilizerSerializer(data=data)
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
            data = FertilizerData.objects.filter().order_by('id')
            serializer = GetFertilizerSerializer(instance=data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)