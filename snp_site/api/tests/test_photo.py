from urllib import response
from django.test import TestCase
from models_app.factories import PhotoFactory,UserFactory
from models_app.models.user import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework.test import APIClient
from django.test.client import encode_multipart



faker=Faker()

class PhotoShowTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.photo = PhotoFactory()
        cls.url='/api/photo/'
        cls.jwt_url='/api/token/' 
        cls.user=UserFactory()       
        token=str(RefreshToken.for_user(cls.user).access_token)


    
    
    def test_view_show_status_200(self):

      
    
        response=self.client.get(f'{self.url}{self.photo.id}/')

        self.assertEqual(response.status_code,200)


    def test_view_show_status_404(self):
        response=self.client.get(f'{self.url}124151233513/')
        self.assertEqual(response.status_code,404)
class PhotoListCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user=UserFactory()       
        cls.token=str(RefreshToken.for_user(cls.user).access_token)
        cls.url='/api/photos/'
    
    def test_photos_list_min_status_200(self):
        response=self.client.get(f'{self.url}')
        self.assertEqual(len(response.data),2)
    
    def test_photos_list_max_status_200(self):
        response=self.client.get(f'{self.url}?page=1&per_page=2&search_field=asd&sort_direction=desc&sort_field=created_at')
        print(response.data)
        self.assertEqual(response.status_code,200)
    def test_create_photo_status_200(self):
        # Создаем тестовые данные
        data = {
            'name': 'ldfasfsdf',
            'description': 'sss',
            'photo': SimpleUploadedFile(name='test_image.png', content=faker.image((20, 20), 'png'), content_type='image/png')
        }

        client = APIClient()
        
    
        response = client.post(
            path=self.url,
            data=data,
            format='multipart',  
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        
        breakpoint()
        self.assertEqual(response.status_code, 200)

class PhotoUpdateDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user=UserFactory()       
        cls.token=str(RefreshToken.for_user(cls.user).access_token)
        cls.photo=PhotoFactory(user=cls.user)
        cls.url=f'/api/photo/actions/'
    def test_update_photo_min_status_200(self):

        data={
            'name':'l',
            'description':'sss',
            'photo': SimpleUploadedFile(name='test_image.png', content=faker.image((20,20),'png'))
        }
        

        client = APIClient()
        content = encode_multipart(
            'dadsfga',
            data
        )
        response=client.put(path=f'{self.url}{self.photo.id}', data=data ,content_type='multipart/form-data; boundary=dadsfga',HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code,200)
    def test_delete_photo_status_200(self):
        headers={
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': 'Bearer ' + self.token
            }
        response=self.client.delete(f'{self.url}{self.photo.id}/', headers=headers)
        self.assertEqual(response.status_code,200)

