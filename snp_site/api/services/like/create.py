from django import forms
from models_app.models import Like, Photo, User
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class CreateLikeService(ServiceWithResult):
    photo_id = forms.IntegerField(required=True, min_value=1)
    current_user = ModelField(User)

    custom_validations = ["_validate_photo_id", "_validate_user_id"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_like()
        return self

    def _create_like(self):

        if Like.objects.filter(
            photo_id=self.cleaned_data["photo_id"],
            user=self.cleaned_data["current_user"],
        ).exists():
            like = Like.objects.get(
                photo_id=self.cleaned_data["photo_id"],
                user=self.cleaned_data["current_user"],
            )
            like.delete()
        else:

            return Like.objects.create(
                photo_id=self.cleaned_data["photo_id"],
                user=self.cleaned_data["current_user"],
            )

        return None

    def _validate_photo_id(self):
        if not Photo.objects.filter(id=self.cleaned_data["photo_id"]).exists():
            self.add_error(
                "id",
                NotFound(
                    message=f'Лайк с id {self.cleaned_data["photo_id"]} не найден '
                ),
            )

    def _validate_user_id(self):
        if not self.cleaned_data["current_user"]:
            self.add_error("current_user", NotFound(message="Пользователь не найден"))
