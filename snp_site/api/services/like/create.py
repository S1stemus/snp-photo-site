from re import M
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Like
from service_objects.errors import NotFound
from models_app.models.user import User
from service_objects.fields import ModelField

class CreateLikeService(ServiceWithResult):
    photo_id=forms.IntegerField(required=True, min_value=1)
    current_user=ModelField(User)
    
    custom_validations = [
        '_validate_like_id',
        '_validate_user_id'
        ]

    def process(self):
        self.run_custom_validations()

    def _create_like(self):
        if Like.objects.filter(id=self.cleaned_data['photo_id'], user=self.cleaned_data['current_user']).exists():
            Like.objects.delete(id=self.cleaned_data['photo_id'], user=self.cleaned_data['current_user'])
        else:
            return Like.objects.create(id=self.cleaned_data['photo_id'], user=self.cleaned_data['current_user'])
            
        return None
    def _validate_like_id(self):
        if not Like.objects.filter(id=self.cleaned_data['photo_id']).exists():
            self.add_error('id', 'Лайк не найден')
    def _validate_user_id(self):
        if not self.cleaned_data['current_user']:
            self.add_error('current_user', 'Пользователь не найден')
    