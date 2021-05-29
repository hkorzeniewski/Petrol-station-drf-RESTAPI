# from app.views import petrol_station_list
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.response import Response
from .models import Fuel, PetrolStation, Price, StationLocation

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['value', 'change_date', 'user']

class FuelSerializer(serializers.ModelSerializer):
    # fuel_price_info = serializers.PrimaryKeyRelatedField(read_only=True)
    fuel_price_info = PriceSerializer()
    class Meta:
        model = Fuel
        fields = ['fuel_type', 'fuel_price_info']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationLocation
        fields = ['voivodeship', 'location_name']

class PetrolStationSerializer(serializers.ModelSerializer):
    fuel = FuelSerializer(many=True)
    location = LocationSerializer(many=True)
    class Meta:
        model = PetrolStation
        fields = ['station_name', 'fuel', 'location']

    def create(self, validated_data):

        raw_fuel = validated_data.pop('fuel')
        raw_location = validated_data.pop('location')
        raw_name = validated_data.pop('station_name')
        # print(raw_fuel)

        for fuel_data in raw_fuel:
            print(fuel_data)
            raw = fuel_data.pop('fuel_price_info')
            price = Price.objects.create(value=raw['value'], user=raw['user'])
            fuel = Fuel.objects.create(fuel_type=fuel_data['fuel_type'], fuel_price_info=price)
            
            fuel_get = Fuel.objects.filter(fuel_type=fuel_data['fuel_type'], fuel_price_info=price)

        for location_data in raw_location:
            location = StationLocation.objects.filter(voivodeship=location_data['voivodeship'], location_name=location_data['location_name'])
        
        petrol_station = PetrolStation.objects.create(station_name=raw_name)
        print(petrol_station)
        petrol_station.fuel.set(fuel_get)
        petrol_station.location.set(location)
        return petrol_station


    # def update(self, instance, validated_data):
        
    #     return super().update(instance, validated_data)