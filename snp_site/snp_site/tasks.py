# myapp/tasks.py

from celery import shared_task
from models_app.models import Photo
from models_app.models.photo.fsm import State


@shared_task
def delete_photo(id):
    photo = Photo.objects.get(id=id)
    if photo.state in [State.ON_DELETE, State.REJECTED]:
        photo.delete()


@shared_task
def print_word(word):
    print(word)


@shared_task
def myprint():
    print("nice")
