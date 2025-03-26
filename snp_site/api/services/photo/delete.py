from datetime import timedelta

from snp_site.tasks import *
from django import forms
from models_app.models import Photo
from models_app.models.user import User
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
import environ

env = environ.Env()
environ.Env.read_env()




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
           photo=Photo.objects.get(id=self.cleaned_data["id"])
           print(photo.state)
           if(photo.state == State.ON_DELETE):
               photo.flow.update_to_waiting()
           else:
               photo.flow.update_to_on_delete()
               delete_photo.apply_async(args = [self.cleaned_data["id"]] , countdown = env('TIME_TO_DELETE_IN_SECONDS',cast=int,default=86400))
           return photo
        except Photo.DoesNotExist:
            return None

    def _validate_photo_id(self):
        photo=Photo.objects.get(id=self.cleaned_data["id"])
        if not photo:
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
