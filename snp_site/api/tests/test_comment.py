from http import client
from urllib import response
from django.test import TestCase
from models_app.factories import UserFactory, PhotoFactory, CommentFactory
from rest_framework_simplejwt.tokens import RefreshToken
from faker import Faker
from rest_framework.test import APIClient
from django.test.client import encode_multipart
from django.contrib.contenttypes.models import ContentType
from models_app.models import Comment,Photo


faker=Faker()
class CommentPostTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.url = '/api/comments/'
        cls.user=UserFactory()
        cls.token=str(RefreshToken.for_user(cls.user).access_token)
        cls.photo=PhotoFactory()
    def test_create_comment_status_200(self):
        data={
            "comment": faker.word(),
            "content_type": "photo",
            "object_id": self.photo.id
            }
        client = APIClient()
        response = client.post(self.url, data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 201)
class CommentShowUpdateDeleteTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.url = '/api/comments/'
        cls.user = UserFactory()
        cls.photo = PhotoFactory(user = cls.user)
        cls.comment = CommentFactory(user = cls.user,object_id = cls.photo.id,content_type = ContentType.objects.get_for_model(Photo),comment = faker.word())
        cls.token=str(RefreshToken.for_user(cls.user).access_token)
    def test_show_comment_status_200(self):
        response = self.client.get(f'{self.url}{self.comment.id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_comment_status_200(self):
        data={
            "comment": faker.word(),
            }
        client = APIClient()

        response = client.put(f'{self.url}{self.comment.id}/', data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(response.status_code, 200)

    def test_delete_comment_status_200(self):
        client = APIClient()
        response=client.delete(path=f'{self.url}{self.comment.id}/',HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code,204)
