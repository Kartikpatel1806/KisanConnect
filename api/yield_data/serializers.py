from rest_framework import serializers
from .models import YieldData,Bot


class YieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldData
        fields = '__all__'

class GetYieldSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = YieldData
        fields = ['id','user_name','image','description','created_at','is_sold',]

    def get_user_name(self, obj):
        return obj.user.name
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y/%m/%d")


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'

class GetBotSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Bot
        fields = ['id','user_name','yield_data','query','created_at',]

    def get_user_name(self, obj):
        return obj.user.name
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y/%m/%d")