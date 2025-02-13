from models_app.models import Like
from rest_framework import serializers


class LikeShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ["photo_id", "user_id", "id"]
