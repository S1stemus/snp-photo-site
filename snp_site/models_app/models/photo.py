from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from .comment import Comment



class Photo (models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE,null=False,blank=False,verbose_name='Пользователь',related_name='photos',related_query_name='photo')
    photo = models.ImageField(upload_to='images/',verbose_name="Фото",null=False,blank=False)
    caption = models.CharField(max_length=100,verbose_name="Описание",null=False,blank=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model_relation=GenericRelation(Comment)
    status=models.CharField(max_length=100,verbose_name="Статус",null=False,blank=False,default="Ожидает модерации")

    class Meta:
        app_label = 'models_app'
        db_table = 'photos'
        verbose_name_plural = 'Фотографии'
        verbose_name = 'Фотография'