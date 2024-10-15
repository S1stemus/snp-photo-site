from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Comment
from service_objects.errors import NotFound
from models_app.models.photo.models import Photo
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from service_objects.fields import ModelField

class CreateCommentService(ServiceWithResult):
    class_dict = {
        'photo': Photo,
        'comment': Comment
    }

    content=forms.CharField(max_length=511, required=True)
    content_type=forms.ChoiceField(choices=(('photo', 'photo'), ('comment', 'comment')))
    object_id=forms.IntegerField( min_value=1)
    current_user=ModelField(User)

    custom_validations = [
        '_validate_comment_id',
        '_validate_user_id'
            ]


    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_comment()
        return self


    def _create_comment(self):
        comment = Comment.objects.create(user=self.cleaned_data['user_id'], comment=self.cleaned_data['content'], content_type=ContentType.objects.get_for_model(self.class_dict[self.cleaned_data['content_type']]), object_id=self.cleaned_data['object_id'])
        return comment

    
    def  _validate_comment_id(self):
        if not Comment.objects.filter(id=self.id).exists():
            self.add_error('id', NotFound(message=f'Комментарий c id {self.id} не найден'))
    def _validate_user_id(self):
        if not self.user_id:
            self.add_error('user', NotFound(message=f'Пользователь с id {self.user_id} не найден'))