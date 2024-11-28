from weakref import ref
from rest_framework import serializers
from models_app.models import Like
class LikePostSerializer(serializers.Serializer):
    photo_id = serializers.IntegerField()
    class Meta:
        fields = ['photo_id']
        ref_name='api_like_create_serializer'