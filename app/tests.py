from app.models import Fuel, Price, StationLocation
from django.test import TestCase, Client, client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate, CoreAPIClient
from rest_framework.authtoken.models import Token
from django.http import response
from rest_framework import status
from requests.auth import HTTPBasicAuth
# Create your tests here.

# token = Token.objects.get(user__username='admin')
# user = User.objects.get(username='admin')

class TestPetrolStation(APITestCase):

    def test_station_list(self):
        client = APIClient()
        response = client.get("http://127.0.0.1:8000/stations/")
        assert response.status_code == 200

    def test_authenticated_can_see_page(self):
        user = User.objects.create_user(username='testuser', password='1234')
        self.client.force_login(user=user)
        response = self.client.get("http://127.0.0.1:8000/")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_can_see_page(self):
        response = self.client.get("http://127.0.0.1:8000/")
        self.assertEqual(response.status_code, 401)

    def test_authenticated_can_add_station(self):
        # client = APIClient(enforce_csrf_checks=True)
        # user = User.objects.get(username='admin')
        user = User.objects.create_user(username='testuser', password='1234')
        token = Token.objects.create(user=user)
        self.client.login(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "id": 1,
            "station_name": "BP",
            "fuel": [
                {
                    "id": 1,
                    "fuel_type": "P98",
                    "fuel_price_info": {
                        "id": 1,
                        "value": "5.82",
                        "change_date": "2021-06-21T22:57:29.760819Z",
                        "user": 1
                    }
                }
                
            ],
            "location": {
                "id": 2,
                "voivodeship": "lubelskie",
                "city_name": "Lublin",
                "street_name": "Zielona 11",
                "x_coordinate": 13.0,
                "y_coordinate": 16.0
            }
        }
        response = self.client.post("http://127.0.0.1:8000/stations/", data, format='json')
        self.assertEqual(response.status_code, 201)
