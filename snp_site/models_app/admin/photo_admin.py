from django.contrib import admin
from models_app.models import Photo
from django.utils.safestring import mark_safe
from models_app.models.photo.fsm import State
from models_app.models.photo.fsm import Flow
from django.contrib import messages



@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    fields = ('user', 'photo','name', 'description','state')
    list_display = ('id','user','name', 'description','state','admin_photo')
    list_filter = ('state','created_at')
    list_display_links = ('user', 'description','name')
    actions = ['approve','reject']
    search_fields = ('user__username','description','name')

    def approve(self, request, queryset):
        for photo in queryset:
            if(photo.state!=State.WAITING):
                messages.add_message(request,messages.WARNING,f'Фото с id {photo.id} уже имеет статус отличный от ожидания')
                continue
            photo.flow.approve()

    def reject(self, request, queryset):
        for photo in queryset:
            if(photo.state!=State.WAITING):
                messages.add_message(request,messages.INFO,f'Фото с id {photo.id} уже имеет статус отличный от ожидания')
                continue
            photo.flow.reject()
        


   
 
    