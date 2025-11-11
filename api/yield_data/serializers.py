from rest_framework import serializers
from .models import YieldData,Query,ChatBot
from django.conf import settings


class YieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldData
        fields = '__all__'

class GetYieldSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = YieldData
        fields = ['id','user_name','user_id','image','description','created_at','is_sold',]

    def get_user_name(self, obj):
        return obj.user.name
    
    def get_user_id(self, obj):
        return obj.user.id
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return f"{settings.MEDIA_URL}{obj.image}"
        return None
    
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