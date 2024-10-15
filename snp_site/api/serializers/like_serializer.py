from rest_framework import serializers
from models_app.models import Like
from api.serializers.photo_serializer import PhotoSerializer

class LikeSerializer(serializers.ModelSerializer):
    photo=PhotoSerializer()
    class Meta:
        model = Like
        fields = ['photo_id','photo', 'user_id', 'id']
        