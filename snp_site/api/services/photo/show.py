from datetime import timedelta
from functools import lru_cache

from api.tasks import print_word
from django import forms
from django.db.models import Count
from models_app.models import Photo
from models_app.models.user import User
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class ShowPhotoService(ServiceWithResult):

    id = forms.IntegerField(min_value=1)
    current_user = ModelField(User, required=False)

    custom_validations = [
        "_validate_photo_id",
        # '_validate_user'
    ]

    def process(self) -> "ServiceWithResult":
        self.run_custom_validations()
        if self.is_valid():
            print_word.apply_async(
                args=["nice"], countdown=timedelta(minutes=1).total_seconds()
            )
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

    def _validate_photo_id(self):
        if not self._photo:
            self.add_error(
                "id",
                NotFound(message=f'Фото c id {self.cleaned_data["id"]} не найдено'),
            )

    def _validate_user(self):
        if self._photo and (
            self.cleaned_data["current_user"].id != self._photo.user.id
            or self._photo.state != Photo.State.APPROVED
        ):
            self.add_error(
                "current_user",
                NotFound(
                    message=f'пользователь {self.cleaned_data["current_user"]} не может просматривать эту фотографию'
                ),
            )
