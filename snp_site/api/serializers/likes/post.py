from rest_framework import serializers


class LikePostSerializer(serializers.Serializer):
    photo_id = serializers.IntegerField()

    class Meta:
        fields = ["photo_id"]
        ref_name = "api_like_create_serializer"
