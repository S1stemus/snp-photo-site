from rest_framework import serializers
from models_app.models import Photo

class PhotoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['photo','name', 'description']