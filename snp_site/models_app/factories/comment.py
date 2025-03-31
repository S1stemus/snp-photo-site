import factory
from models_app.models import Comment
from faker import Faker

from snp_site.api.views import photo

faker=Faker()

class CommentFactory(factory.django.DjangoModelFactory):
    comment=faker.word()
    user=factory.SubFactory('models_app.factories.user.UserFactory')
    class Meta:
        model= Comment