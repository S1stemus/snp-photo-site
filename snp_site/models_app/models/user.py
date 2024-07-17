from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
