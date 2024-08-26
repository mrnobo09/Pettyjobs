from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Job,JobImages

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','username','full_name','user_type','sub_type','password')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','full_name','user_type','is_active','is_staff']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id','title','job_type','location','description','status','approved_by','accepted_by']

class JobImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobImages
        fields = ['job','image','uploaded_at']

    