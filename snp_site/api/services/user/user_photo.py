from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import User
from service_objects.fields import ModelField
from models_app.models.photo.models import Photo
from models_app.models.photo.fsm import State




class UserPhotoService(ServiceWithResult):
    user_id = forms.IntegerField(min_value=1)
    current_user = ModelField(User,required=False)

    custom_validations = [
        '_validate_user'
    ]

    def _validate_user(self):
        if not User.objects.filter(id=self.cleaned_data['user_id']).exists():
            self.add_error('user', 'Пользователь не найден')

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._user_photo
        return self
    @property
    def _user_photo(self):
        if User.objects.get(id=self.cleaned_data['user_id']) == self.cleaned_data['current_user']:           
            return Photo.objects.filter(user=self.cleaned_data['user_id'])
        else:
            photos = Photo.objects.filter(user=self.cleaned_data['user_id'])
            return photos.filter(state=State.APPROVED)