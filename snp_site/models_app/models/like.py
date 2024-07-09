from django.db import models
class Like(models.Model):
    photo_id = models.ForeignKey('Photo', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    class Meta:
        app_label = 'models_app'