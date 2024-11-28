from rest_framework import serializers
from models_app.models import Like

class LikeSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj)->int:
        return obj.likes.count()
    class Meta:
        model = Like
        fields = ['photo_id', 'user_id', 'id', 'like_count']
        