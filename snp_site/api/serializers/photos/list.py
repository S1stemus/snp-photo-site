from api.serializers.user.show import UserSerializer
from models_app.models import Photo
from rest_framework import serializers


class PhotoListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    user = UserSerializer()

    class Meta:
        model = Photo
        fields = [
            "id",
            "photo",
            "name",
            "description",
            "user",
            "state",
            "like_count",
            "comment_count",
        ]
