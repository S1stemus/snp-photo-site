from rest_framework import serializers
from models_app.models import Photo
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'