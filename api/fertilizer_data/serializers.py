from rest_framework import serializers
from .models import FertilizerData


class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilizerData
        fields = '__all__'

class GetFertilizerSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = FertilizerData
        fields = ['id','user_name','nitrogen','phosphorus','potassium','temperature','humidity','soil_moisture','soil_type','crop_type','result']

    def get_user_name(self, obj):
        return obj.user.name