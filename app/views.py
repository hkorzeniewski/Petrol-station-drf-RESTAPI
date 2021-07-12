from django.contrib.auth.models import User
from django.db.models import fields
from app.serializers import LocationDetailSerializer, PetrolStationSerializer, PriceDetailSerializer, UserSerializer, FuelDetailSerializer
from app.models import PetrolStation
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework import permissions, status
from .models import Fuel, PetrolStation, Price, StationLocation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django.http import JsonResponse, Http404
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.core.serializers import serialize

from app import models

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'stations': reverse('station-list', request=request, format=format)
    })

class PriceDetail(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceDetailSerializer


class StationLocationList(viewsets.ModelViewSet):
    queryset = StationLocation.objects.all()
    serializer_class = LocationDetailSerializer


class PetrolStationList(generics.ListAPIView):
    queryset = PetrolStation.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PetrolStationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station_name', 'location__city_name', 'location__voivodeship', "fuel__fuel_type"]
    ordering = ['station_name']
    
    def post(self, request, format=None):
        serializer = PetrolStationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PetrolStationDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return PetrolStation.objects.get(pk=pk)
        except PetrolStation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        petrol_station = self.get_object(pk)
        serializer = PetrolStationSerializer(petrol_station)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        petrol_station = self.get_object(pk)
        serializer = PetrolStationSerializer(petrol_station, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PetrolStationAddFuelViewSet(viewsets.ModelViewSet):
    queryset = models.PetrolStation.objects.all()
    serializer_class = PetrolStationSerializer

    @action(methods=['post', 'get'], detail=True)
    def add_fuel(self, request, *args, **kwargs):
        obj = self.get_object()
        station = PetrolStation.objects.get(id=obj.id)
        request_fuels=request.data

        if 'fuel' in request_fuels:
            print('jadom')
            for fuel in request_fuels['fuel']:
                price = Price.objects.create(
                    value=fuel['fuel_price_info']['value'], user=request.user)
                fuel1 = Fuel.objects.create(
                    fuel_type=fuel['fuel_type'], fuel_price_info=price)
                station.fuel.add(fuel1)
                station.save()
            return Response("Successfully added fuels")
        return Response("Bonk")


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
