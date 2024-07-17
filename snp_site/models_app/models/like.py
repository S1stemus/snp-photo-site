from django.db import models  


class Like(models.Model):
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE,null=False,blank=False,verbose_name='Фото',related_name='likes',related_query_name='like')
    user = models.ForeignKey('User', on_delete=models.CASCADE,null=False,blank=False,verbose_name='Пользователь',related_name='likes',related_query_name='like')
    class Meta:
        app_label = 'models_app'
        db_table = 'likes'
        unique_together = ('photo', 'user')
        verbose_name_plural = 'Лайки'
        verbose_name = 'Лайк'

