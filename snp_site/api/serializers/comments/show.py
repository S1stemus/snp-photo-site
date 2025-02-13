from api.serializers.user.show import UserSerializer
from models_app.models import Comment
from rest_framework import serializers


class CommentShowSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "user",
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        ]
