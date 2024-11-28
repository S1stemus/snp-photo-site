from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo
from service_objects.errors import NotFound
from rest_framework.response import Response
from rest_framework import status
from models_app.models.user import User
from service_objects.fields import ModelField

class DeletePhotoService(ServiceWithResult):

    id=forms.IntegerField(min_value=1)
    current_user=ModelField(User)

    custom_validations = [
        '_validate_photo_id'
        ]

    def process(self) -> "ServiceWithResult":
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._photo 
        return self
    @property
    def _photo(self):
        try:
           photo=Photo.objects.get(id=self.cleaned_data['id'])
           photo.delete()
           return (photo)
        except Photo.DoesNotExist:
            return None

    def _validate_photo_id(self):
        if not self._photo:
            self.add_error('id', NotFound(message=f'Фото c id {self.cleaned_data["id"]} не найдено'))

    def _validated_user(self):
        if self.cleaned_data['current_user'] != Photo.objects.get(id=self.cleaned_data['id']).user:
            self.add_error('user', NotFound(message=f'Фото с id {self.cleaned_data["id"]} не принадлежит пользователю {self.cleaned_data["current_user"]}'))        