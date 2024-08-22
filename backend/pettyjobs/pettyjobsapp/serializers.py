from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','username','full_name','user_type','password')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','full_name','user_type','is_active','is_staff']

    