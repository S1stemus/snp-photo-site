from models_app.models import Photo
from rest_framework import serializers


class PhotoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["photo", "name", "description"]
