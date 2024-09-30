from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars', verbose_name="Аватар", null=True, blank=True)
    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
    
    
