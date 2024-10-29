from models_app.models.comment import Comment
from rest_framework import serializers

class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']