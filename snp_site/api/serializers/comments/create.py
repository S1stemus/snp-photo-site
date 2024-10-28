from models_app.models.comment import Comment
from rest_framework import serializers

class CommentCreateSerializer(serializers.ModelSerializer):
    content_type=serializers.CharField()

    class Meta:
        model = Comment
        fields = ['comment','user','content_type','object_id']