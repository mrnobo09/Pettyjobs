from djoser.serializers import UserCreateSerializer
from io import BytesIO
from PIL import Image
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Job,JobImages
import base64

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','username','full_name','user_type','sub_type','password')
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','full_name','user_type','is_active','is_staff']



class JobImagesSerializer(serializers.ModelSerializer):
    image_data = serializers.SerializerMethodField()

    class Meta:
        model = JobImages
        fields = ['job', 'image_data', 'uploaded_at']

    def get_image_data(self, obj):
        if obj.image:
            with obj.image.open('rb') as f:
                image = Image.open(f)
                
                # Resize image
                max_size = (800, 800)  # Adjust max size as needed
                image.thumbnail(max_size)

                # Reduce quality
                buffer = BytesIO()
                image = image.convert('RGB')
                image.save(buffer, format='JPEG', quality=50)  # Adjust quality as needed
                image_data = buffer.getvalue()
                
            return base64.b64encode(image_data).decode('utf-8')
        
        return None

    
class JobSerializer(serializers.ModelSerializer):
    images = JobImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'job_type', 'location', 'description', 'status', 'approved_by', 'accepted_by', 'uploaded_at', 'approved_at', 'completed_at', 'images']

    