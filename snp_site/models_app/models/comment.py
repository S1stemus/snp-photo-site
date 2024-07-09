from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class Comment (models.Model):
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None) 
    object_id = models.PositiveIntegerField(default=None)
    object= GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'models_app'