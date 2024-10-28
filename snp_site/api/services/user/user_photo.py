from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import User
from service_objects.fields import ModelField
from models_app.models.photo import Photo



class UserPhotoService(ServiceWithResult):
    user = forms.IntegerField(min_value=1)
    current_user = ModelField(User, required=False)

    custom_validations = [
        '_validate_user'
    ]

    def _validate_user(self):
        if not User.objects.filter(id=self.cleaned_data['user']).exists():
            self.add_error('user', 'Пользователь не найден')

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._user_photo
        return self
    @property
    def _user_photo(self):
        if User.objects.get(id=self.cleaned_data['user']) == self.cleaned_data['current_user']:
            return Photo.objects.filter(user=self.cleaned_data['user'])
        else:
            photos = Photo.objects.filter(user=self.cleaned_data['user'])
            return photos.filter(state=photos.State.APPROVED)