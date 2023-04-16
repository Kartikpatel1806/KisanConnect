from rest_framework import serializers
from .models import CropData


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropData
        fields = '__all__'

class GetCropSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = CropData
        fields = ['id','user_name','nitrogen','phosphorus','potassium','temperature','humidity','ph','rainfall','result']

    def get_user_name(self, obj):
        return obj.user.name