from app.serializers import PetrolStationSerializer
from app.models import PetrolStation
from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework import permissions, status
from .models import PetrolStation
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

# class PetrolStationViewsSet(viewsets.ModelViewSet):
#     queryset = PetrolStation.objects.all()
#     serializer_class = PetrolStationSerializer

@api_view(['GET', 'POST'])
def petrol_station_list(request):
    if request.method == 'GET':
        stations = PetrolStation.objects.all()
        serializer = PetrolStationSerializer(stations, many= True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        
        serializer = PetrolStationSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)