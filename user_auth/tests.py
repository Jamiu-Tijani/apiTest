import email
from unicodedata import name
from django.test import TestCase
from django.contrib.auth.models import User

from user_auth.views import userReg

# Create your tests here.
from .models import userData
from django.urls import path, reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json
from django.test.client import Client
from rest_framework.test import APIClient


class userDataTestCase(TestCase):
    def setUp(self):
        userData.objects.create(username= "John" , email= "johndoe@johdoe.com", password = "@John1243")  
        userData.objects.create(username= "Lorem" , email= "loremIpsum@lorem.com", password = "@loren1243") 
    def test_user_created(self):
        john = userData.objects.get(username = "John")
        lorem = userData.objects.get(username = "Lorem")

        self.assertEqual(john.email, "johndoe@johdoe.com")
        self.assertEqual(lorem.email, "loremIpsum@lorem.com")
   
    def test_user_cannot_register_with_no_data(self):
        url= reverse('data')
        res = self.client.post(url)
        self.assertEqual(res.status_code, 403)
    

    
    def test_get_token(self):
        # test that jwt token is returned
         myadmin = User.objects.create_superuser(username = "ade",password ="@adeola123")
         c = Client()
         c.login(username = myadmin.username, password = myadmin.password)
         
         url = reverse("token_obtain_pair")
         data = {
             "username" : "ade",
             "password" : "@adeola123"
         }
         response = self.client.post(url, data, content_type="application/json")
         response_content = json.loads(response.content.decode('utf-8'))
         token = response_content["access"]
         self.assertEqual(response.status_code, 200, "The token should be successfully returned.")
         return token
    
    def test_user_created_request(self):
        # test that user can be created through api with jwt token
         myadmin = User.objects.create_superuser(username = "ade",password ="@adeola123")
         c = Client()
         c.login(username = myadmin.username, password = myadmin.password)
         
         url = reverse("token_obtain_pair")
         data = {
             "username" : "ade",
             "password" : "@adeola123"
         }
         response = self.client.post(url, data, content_type="application/json")
         response_content = json.loads(response.content.decode('utf-8'))
         token = response_content["access"]
         rurl = reverse('data')
         data = {'username': 'Chuku', "email": "emeka@gmail.com","password": "@chukuemeka123"}
         cli = APIClient()
         cli.credentials(HTTP_AUTHORIZATION= 'Bearer  {}'.format(token))
         rresponse = cli.post(rurl, data,format = 'json')
         self.assertEqual(rresponse.status_code, status.HTTP_201_CREATED)

    def test_user_not_created_request(self):
        # test that user can't be created through api without with jwt token
         url = reverse('data')
         data = {'username': 'Chuku', "email": "emeka@gmail.com","password": "@chukuemeka123"}
         rresponse = self.client.post(url, data,format = 'json')
         self.assertEqual(rresponse.status_code, status.HTTP_403_FORBIDDEN, "Authentication credentials not provided")

    def test_username_modified(self):
         myadmin = User.objects.create_superuser(username = "ade",password ="@adeola123")
         c = Client()
         c.login(username = myadmin.username, password = myadmin.password)
         
         url = reverse("token_obtain_pair")
         data = {
             "username" : "ade",
             "password" : "@adeola123"
         }
         response = self.client.post(url, data, content_type="application/json")
         response_content = json.loads(response.content.decode('utf-8'))
         token = response_content["access"]
         rurl = reverse('MOD')
         data = {'username': 'Chuku',"password": "@chukuemeka123","new_username": "chuks"}
         cli = APIClient()
         cli.credentials(HTTP_AUTHORIZATION= 'Bearer  {}'.format(token))
         rresponse = cli.post(rurl, data,format = 'json')
         self.assertEqual(rresponse.status_code, status.HTTP_201_CREATED)
