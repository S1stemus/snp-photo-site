from urllib import request
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo
from service_objects.errors import NotFound
from models_app.models.user import User
from service_objects.fields import ModelField


class UpdatePhotoService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)
    photo = forms.ImageField(required=False)
    caption = forms.CharField(max_length=127, required=False)
    current_user = ModelField(User)

    
    custom_validations = [
        '_validate_photo_id',
        '_validate_user'
    ]
    

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._photo
        return self
    @property
    def _photo(self):
        try:
            image = Photo.objects.get(id=self.cleaned_data['id'])
            image.caption = self.cleaned_data['caption']
            image.photo = self.cleaned_data['photo']
            image.save()
            return image
        
        except Photo.DoesNotExist:
            return None

    def _validate_photo_id(self):
        if not self._photo:
            self.add_error('id', NotFound(message=f'Фото с id {self.cleaned_data["id"]} не найдено'))
    def _validate_user(self):
        if self.cleaned_data['current_user'] != Photo.objects.get(id=self.cleaned_data['id']).user:
            self.add_error('user', NotFound(message=f'Фото с id {self.cleaned_data["id"]} не принадлежит пользователю {self.cleaned_data["current_user"]}'))