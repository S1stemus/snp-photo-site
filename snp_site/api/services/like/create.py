from django import forms
from models_app.models import Like, Photo, User
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
import channels.layers
from asgiref.sync import async_to_sync


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
        photo=Photo.objects.get(id=self.cleaned_data['photo_id'])

        if Like.objects.filter(
            photo_id=self.cleaned_data["photo_id"],
            user=self.cleaned_data["current_user"],
        ).exists():
            like = Like.objects.get(
                photo_id=self.cleaned_data["photo_id"],
                user=self.cleaned_data["current_user"],
            )
            like.delete()
            if(photo.user.id != self.cleaned_data['current_user'].id):
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    str(photo.user.id),
                    {
                        "type": "create",
                        "message": f"Пользователь {photo.user.username} убрал лайк. Сейчас лайков {photo.likes.count()}"
                    },
                )
            
        else:
            if(photo.user.id != self.cleaned_data['current_user'].id):
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    str(photo.user.id),
                    {
                        "type": "create",
                        "message": f"Пользователь {self.cleaned_data['current_user'].username}  оценил вашу фотографию. Сейчас лайков {photo.likes.count()+1}"
                    },
                )
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
