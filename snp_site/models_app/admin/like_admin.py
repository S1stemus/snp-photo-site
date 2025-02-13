from django.contrib import admin
from models_app.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    fields = ("photo", "user")
