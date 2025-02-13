from datetime import timedelta

from api.tasks import delete_photo
from django import forms
from models_app.models import Photo
from models_app.models.user import User
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class DeletePhotoService(ServiceWithResult):

    id = forms.IntegerField(min_value=1)
    current_user = ModelField(User)

    custom_validations = ["_validate_photo_id"]

    def process(self) -> "ServiceWithResult":
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._photo
        return self

    @property
    def _photo(self):
        try:
            delete_photo.apply_async(
                self.cleaned_data["id"], countdown=timedelta(minutes=1)
            )
        except Photo.DoesNotExist:
            return None

    def _validate_photo_id(self):
        if not self._photo:
            self.add_error(
                "id",
                NotFound(message=f'Фото c id {self.cleaned_data["id"]} не найдено'),
            )

    def _validated_user(self):
        if (
            self.cleaned_data["current_user"]
            != Photo.objects.get(id=self.cleaned_data["id"]).user
        ):
            self.add_error(
                "user",
                NotFound(
                    message=f'Фото с id {self.cleaned_data["id"]} не принадлежит '
                    f'пользователю {self.cleaned_data["current_user"]}'
                ),
            )
