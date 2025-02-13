from django import forms
from models_app.models import Comment
from models_app.models.user import User
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class UpdateCommentService(ServiceWithResult):

    id = forms.IntegerField(min_value=1)
    comment = forms.CharField(max_length=511, required=True)
    current_user = ModelField(User)

    custom_validations = ["_validate_comment_id", "_validate_user"]

    def process(self) -> "ServiceWithResult":
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_comment
        return self

    @property
    def _update_comment(self):
        comment = Comment.objects.get(id=self.cleaned_data["id"])
        comment.comment = self.cleaned_data["comment"]
        comment.save()
        return comment

    def _validate_comment_id(self):
        if not Comment.objects.filter(id=self.cleaned_data["id"]).exists():
            self.add_error(
                "id", NotFound(message=f'Объект {self.cleaned_data["id"]} не найден ')
            )

    def _validate_user(self):
        if (
            self.cleaned_data["current_user"].id
            != Comment.objects.get(id=self.cleaned_data["id"]).user.id
        ):
            self.add_error(
                "current_user",
                NotFound(
                    message=f'пользователь {self.cleaned_data["current_user"]} не может редактировать этот комментарий'
                ),
            )
