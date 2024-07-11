from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from .comment import Comment


class Photo (models.Model):
    photo = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model_relation=GenericRelation(Comment)

    class Meta:
        app_label = 'models_app'
        db_table = 'photos'
