import factory
from models_app.models import Comment,Photo
from faker import Faker
from django.contrib.contenttypes.models import ContentType



faker=Faker()

class CommentFactory(factory.django.DjangoModelFactory):
    comment=faker.word()
    object_id=factory.Sequence(lambda n: n)
    user=factory.SubFactory('models_app.factories.user.UserFactory')
    class Meta:
        model= Comment