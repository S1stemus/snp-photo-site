import channels.layers
from asgiref.sync import async_to_sync
from django.db import models


class Notification(models.Model):
    text = models.CharField(
        max_length=511, verbose_name="Текст", null=False, blank=False
    )

    def save(self, *args, **kwargs):
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "users",
            {"type": "create", "message": self.text},
        )
        super().save(*args, **kwargs)

    class Meta:
        app_label = "models_app"
        db_table = "notification"
        verbose_name_plural = "Уведомления"
        verbose_name = "Уведомление"
