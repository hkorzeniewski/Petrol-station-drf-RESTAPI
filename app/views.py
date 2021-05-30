import rest_framework
from app.serializers import LocationDetailSerializer, PetrolStationSerializer, PriceDetailSerializer
from app.models import PetrolStation
from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework import permissions, status
from .models import PetrolStation, Price, StationLocation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from rest_framework import generics

# Create your views here.
class PriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceDetailSerializer


class StationLocationList(generics.RetrieveUpdateDestroyAPIView):
    queryset = StationLocation.objects.all()
    serializer_class = LocationDetailSerializer

class PetrolStationList(APIView):
    
    def get(self, request, format=None):
        stations = PetrolStation.objects.all()
        serializer = PetrolStationSerializer(stations, many= True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PetrolStationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PetrolStationDetail(APIView):
    
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
    
