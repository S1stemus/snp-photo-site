from django.db import models
class User(models.Model):
    username = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'models_app'