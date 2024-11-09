from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Comment
from service_objects.errors import NotFound
from models_app.models.user import User
from service_objects.fields import ModelField
from django.core.exceptions import ObjectDoesNotExist

class DeleteCommentService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)
    current_user = ModelField(User)
    custom_validations = [
        '_validate_comment_id',
        '_validated_user',
        '_validate_comments_exist'
    ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_comment
        return self

    @property
    def _delete_comment(self):       
        com= self._comment
        com.delete()
                    
    @property
    def _comment(self):
        try:
            return Comment.objects.get(id=self.cleaned_data['id'])
        except ObjectDoesNotExist:
            return None
       
    
    def _validate_comment_exist(self):
        if not self._comment :
            self.add_error('id', NotFound(message=f'Комментарий с id {self.cleaned_data["id"]} не найден'))
    def _validated_user(self):
        if self.cleaned_data['current_user'].id != self._comment.user.id:
            self.add_error('current_user', NotFound(message=f'пользователь {self.cleaned_data["current_user"]} не может удалить этот комментарий'))
    def _validate_comments_exist(self):
        if  self._comment.model_relation.all().count() != 0 :
            self.add_error('id', NotFound(message=f'Комментарий с id {self.cleaned_data["id"]} имеет комментарии'))