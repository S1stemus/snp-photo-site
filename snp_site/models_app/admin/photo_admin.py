from api.tasks import delete_photo
from django.contrib import admin, messages
from models_app.models import Photo
from models_app.models.photo.fsm import State


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    fields = ("user", "photo", "name", "description", "state")
    list_display = ("id", "user", "name", "description", "state", "admin_photo")
    list_filter = ("state", "created_at")
    list_display_links = ("user", "description", "name")
    actions = ["approve", "reject"]
    search_fields = ("user__username", "description", "name")

    def approve(self, request, queryset) -> None:
        for photo in queryset:
            if photo.state != State.WAITING:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f"Фото с id {photo.id} уже имеет статус отличный от ожидания",
                )
                continue
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
            photo.flow.reject()
            delete_photo(photo.id)
