from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
        
class UserSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id','email','role','name','is_active','is_kyc','is_staff','is_superuser','password',)


class SuperUserSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id','email','role','name','password','is_active','is_kyc','is_staff','is_superuser',)