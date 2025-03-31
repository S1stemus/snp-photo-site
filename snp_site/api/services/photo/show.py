from functools import lru_cache

from django import forms
from django.db.models import Count
from models_app.models import Photo
from models_app.models.photo.fsm import State
from models_app.models.user import User
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class ShowPhotoService(ServiceWithResult):

    id = forms.IntegerField(min_value=1)
    current_user = ModelField(User, required=False)
    custom_validations = ["_validate_photo_id", "_validate_user"]

    def process(self) -> "ServiceWithResult":
        self.run_custom_validations()
        self.result = self._photo
        return self

    @property
    @lru_cache
    def _photo(self):
        try:
            return (
                Photo.objects.filter(id=self.cleaned_data["id"])
                .annotate(comment_count=Count("model_relation"))
                .annotate(like_count=Count("like"))
                .select_related("user")
                .first()
            )
        except Photo.DoesNotExist:
            return None

    def _validate_user(self):
        if self._photo:
            if (self.cleaned_data["current_user"] != self._photo.user) and (
                self._photo.state != State.APPROVED
            ):
                self.add_error(
                    "current_user",
                    NotFound(
                        message=f'пользователь {self.cleaned_data["current_user"]}'
                        f"не может просматривать эту фотографию"
                    ),
                )

    def _validate_photo_id(self):
        if not self._photo:
            self.add_error(
                "id",
                NotFound(message=f'Фото c id {self.cleaned_data["id"]} не найдено'),
            )
