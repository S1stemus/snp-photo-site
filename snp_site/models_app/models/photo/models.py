from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ..comment import Comment
from models_app.models.photo.fsm import State, Flow
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe




class Photo(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE,null=False,blank=False,verbose_name='Пользователь',related_name='photos',related_query_name='photo')
    photo = models.ImageField(upload_to='images/', verbose_name="Фото", null=False,blank=False,validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    # prev_photo = models.ImageField(upload_to='images/', verbose_name="Предыдущее фото", null=True,blank=False,validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    description = models.CharField(max_length=127, verbose_name="Описание" ,null=False,blank=False) 
    # prev_description = models.CharField(max_length=127, verbose_name="Предыдущее описание" ,null=True,blank=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model_relation=GenericRelation(Comment)
    state=models.CharField(max_length=31, verbose_name="Статус", null=False, blank=False, default=State.WAITING, choices=State.choices)

    class Meta:
        app_label = 'models_app'
        db_table = 'photos'
        verbose_name_plural = 'Фотографии'
        verbose_name = 'Фотография'
    @property
    def flow(self):
        return Flow(self)
    
    def admin_photo(self):
        return mark_safe(f'<img src="{self.photo.url}" width="400" height=auto />')
    admin_photo.short_description = 'Фото'
    admin_photo.allow_tags = True