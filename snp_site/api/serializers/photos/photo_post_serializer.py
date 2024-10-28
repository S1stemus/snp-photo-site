from rest_framework import serializers
from models_app.models import Photo

class PhotoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['photo', 'caption']