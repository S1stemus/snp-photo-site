from django.contrib import admin
from models_app.models.notification import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    fields = ["text"]
    list_display = ["text"]
