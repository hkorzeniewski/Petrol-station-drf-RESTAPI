from django.contrib.auth.models import User
from app.serializers import LocationDetailSerializer, PetrolStationSerializer, PriceDetailSerializer, UserSerializer
from app.models import PetrolStation
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework import permissions, status
from .models import PetrolStation, Price, StationLocation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django.http import JsonResponse, Http404
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

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
    filterset_fields = ['station_name']
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