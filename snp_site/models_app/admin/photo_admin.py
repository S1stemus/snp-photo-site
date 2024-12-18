from django.contrib import admin
from models_app.models import Photo
from django.utils.safestring import mark_safe
from models_app.models.photo.fsm import State
from models_app.models.photo.fsm import Flow



@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    fields = ('user', 'photo', 'description','state')
    list_display = ('user', 'description','state','admin_photo')
    list_filter = ('user', 'state','created_at')
    list_display_links = ('user', 'description')
    actions = ['approve','reject']

    def approve(self, request, queryset):
        for photo in queryset:
            photo.approve()

    def reject(self, request, queryset):
        queryset.reject()


   
 
    