from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class Comment (models.Model):
    comment = models.CharField(max_length=255,verbose_name="Комментарий",null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) 
    object_id = models.PositiveIntegerField()
    object= GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'models_app'
        db_table = 'comments'
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'