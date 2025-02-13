from django import forms
from models_app.models import User
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult


class UserUpdateService(ServiceWithResult):
    user_id = forms.IntegerField(min_value=1)
    username = forms.CharField(max_length=127, required=False)
    avatar = forms.ImageField(required=False)

    current_user = ModelField(User)

    custom_validations = ["_validate_user_id", "_validate_user"]

    def _validate_user_id(self):
        if not User.objects.filter(id=self.cleaned_data["user_id"]).exists():
            self.add_error("user_id", "Нет такого пользователя")

    def _validate_user(self):
        if self.cleaned_data["current_user"] != User.objects.get(
            id=self.cleaned_data["user_id"]
        ):
            self.add_error(
                "current_user",
                "Вы не можете редактировать профиль другого пользователя",
            )

    def process(self) -> "ServiceWithResult":
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_user
        return self

    @property
    def _update_user(self):
        user = User.objects.get(id=self.cleaned_data["user_id"])
        user.username = self.cleaned_data["username"]
        user.avatar = self.cleaned_data["avatar"]
        user.save()
        return user
