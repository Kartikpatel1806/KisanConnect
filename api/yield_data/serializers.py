from rest_framework import serializers
from .models import YieldData,Query,ChatBot


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


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'

class GetQuerySerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Query
        fields = ['id','user_name','yield_data','query','created_at',]

    def get_user_name(self, obj):
        return obj.user.name
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y/%m/%d")
    

class ChatBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBot
        fields = '__all__'

class GetChatBotSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = ChatBot
        fields = ['id','user_name','answer','query','created_at',]

    def get_user_name(self, obj):
        return obj.user.name
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y/%m/%d")