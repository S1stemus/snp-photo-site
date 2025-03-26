from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from models_app.models import Photo
from models_app.models.photo.fsm import State
import channels.layers
from asgiref.sync import async_to_sync
from snp_site.tasks import delete_photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    fields = ("user", "photo", "name", "description", "state")
    list_display = (
        "id",
        "user",
        "name",
        "description",
        "prev_description",
        "state",
        "admin_photo",
        "admin_prev_photo",
        
    )
    list_filter = ("state", "created_at")
    list_display_links = ("user", "description", "name")
    actions = ["approve", "reject"]
    search_fields = ("user__username", "description", "name")

    def admin_photo(self, obj):
        return mark_safe(
            f'<img src="{obj.photo.url}" width="400" height=auto />'
        )  # nosec

    def admin_prev_photo(self, obj):
        print(obj.prev_photo)
        if not obj.prev_photo:
            return ""
        return mark_safe(
            f'<img src="{obj.prev_photo.url}" ' f'width="400" height=auto />'
        )  # nosec

    admin_photo.short_description = "Фото"
    admin_photo.allow_tags = True

    def approve(self, request, queryset) -> None:
        for photo in queryset:
            if photo.state != State.WAITING:
                
                messages.add_message(
                    request,
                    messages.WARNING,
                    f"Фото с id {photo.id} уже имеет статус отличный от ожидания",
                )
                continue
            channel_layer = channels.layers.get_channel_layer()
            print(photo.user.id)
            async_to_sync(channel_layer.group_send)(
                str(photo.user.id),
                {
                    "type": "create",
                    "message": f"Фотогорафию {photo.name}  одобрили"
                },
            )
            photo.flow.approve()

    def reject(self, request, queryset):
        for photo in queryset:
            if photo.state != State.WAITING:
                
                messages.add_message(
                    request,
                    messages.INFO,
                    f"Фото с id {photo.id} уже имеет статус отличный от ожидания",
                )
                continue
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                str(photo.user.id),
                {
                    "type": "create",
                    "message": f"Фотогорафию {photo.name}  отклонили"
                },
            )
            photo.flow.reject()  
            delete_photo(photo.id)
