from django import forms
from django.contrib.contenttypes.models import ContentType
from models_app.models import Comment
from models_app.models.photo.models import Photo
from models_app.models.user import User
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class CreateCommentService(ServiceWithResult):
    class_dict = {"photo": Photo, "comment": Comment}

    comment = forms.CharField(max_length=511, required=True)
    content_type = forms.ChoiceField(
        choices=(("photo", "photo"), ("comment", "comment"))
    )
    object_id = forms.IntegerField(min_value=1)
    current_user = ModelField(User)

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_comment
        return self

    @property
    def _create_comment(self):
        comment = Comment.objects.create(
            user=self.cleaned_data["current_user"],
            comment=self.cleaned_data["comment"],
            content_type=ContentType.objects.get_for_model(
                self.class_dict[self.cleaned_data["content_type"]]
            ),
            object_id=self.cleaned_data["object_id"],
        )
        return comment
