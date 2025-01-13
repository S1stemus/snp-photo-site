from functools import lru_cache
from urllib import request
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo
from service_objects.errors import NotFound
from models_app.models.user import User
from service_objects.fields import ModelField
from models_app.models.photo.fsm import State
from models_app.models.photo.fsm import Flow


class UpdatePhotoService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)
    photo = forms.ImageField(required=False)
    description = forms.CharField(max_length=127, required=False)
    name = forms.CharField(max_length=127, required=False)
    current_user = ModelField(User)

    
    custom_validations = [
        '_validate_photo_id',
        '_validate_user'
    ]
    

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._update_photo()
            self.result = self._photo
        return self
    
    @property
    @lru_cache
    def _photo(self):
        try:                                        
            return Photo.objects.get(id=self.cleaned_data['id'])        
        except Photo.DoesNotExist:
            return None
    def _update_photo(self):       
        description = self.cleaned_data['description']
        photo = self.cleaned_data['photo']
        name=self.cleaned_data['name']
        prev_photo=self._photo.photo
        prev_name=self._photo.name
        prev_description=self._photo.description
        self._photo.photo=photo
        self._photo.name=name
        self._photo.description=description
        self._photo.prev_photo=prev_photo
        self._photo.prev_name=prev_name
        self._photo.prev_description=prev_description
        self._photo.flow.update_to_waiting()



    def _validate_photo_id(self):
        if not self._photo:
            self.add_error('id', NotFound(message=f'Фото с id {self.cleaned_data["id"]} не найдено'))
    def _validate_user(self):
        if self.cleaned_data['current_user'] != Photo.objects.get(id=self.cleaned_data['id']).user:
            self.add_error('user', NotFound(message=f'Фото с id {self.cleaned_data["id"]} не принадлежит пользователю {self.cleaned_data["current_user"]}'))