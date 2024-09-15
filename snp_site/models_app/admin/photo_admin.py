from django.contrib import admin
from models_app.models import Photo

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    fields = ('user', 'photo', 'caption','status')