from rest_framework import serializers
from models_app.models import Like

class LikeShowSerializer(serializers.ModelSerializer):
    

    
    class Meta:
        model = Like
        fields = ['photo_id', 'user_id', 'id']
        