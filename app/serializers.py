# from app.views import petrol_station_list
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.response import Response
from .models import Fuel, PetrolStation, Price, StationLocation
from django.utils import timezone

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['value']


class PriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'value', 'change_date', 'user']
    
    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        return instance


class FuelSerializer(serializers.ModelSerializer):
    fuel_price_info = PriceDetailSerializer()
    class Meta:
        model = Fuel
        fields = ['fuel_type', 'fuel_price_info']


class FuelDetailSerializer(serializers.ModelSerializer):
    fuel_price_info = PriceDetailSerializer()
    class Meta: 
        model = Fuel
        fields = ['fuel_type', 'fuel_price_info']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationLocation
        fields = ['voivodeship', 'city_name']


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationLocation
        fields = ['id', 'voivodeship', 'city_name', 'street_name', 'x_coordinate', 'y_coordinate']


class PetrolStationSerializer(serializers.ModelSerializer):
    fuel = FuelDetailSerializer(many=True)
    location = LocationDetailSerializer(many=True)
    class Meta:
        model = PetrolStation
        fields = ['station_name', 'fuel', 'location']

    def create(self, validated_data):

        raw_fuel = validated_data.pop('fuel')
        raw_location = validated_data.pop('location')
        raw_name = validated_data.pop('station_name')

        for fuel_data in raw_fuel:
            raw = fuel_data.pop('fuel_price_info')
            price = Price.objects.create(value=raw['value'], user=raw['user'])
            fuel = Fuel.objects.create(fuel_type=fuel_data['fuel_type'], fuel_price_info=price)
            
            fuel_get = Fuel.objects.filter(fuel_type=fuel_data['fuel_type'], fuel_price_info=price)

        for location_data in raw_location:
            location = StationLocation.objects.filter(voivodeship=location_data['voivodeship'], city_name=location_data['city_name'])
        
        petrol_station = PetrolStation.objects.create(station_name=raw_name)
        petrol_station.fuel.set(fuel_get)
        petrol_station.location.set(location)
        return petrol_station


    def update(self, instance, validated_data):
        instance.station_name = validated_data.get('station_name', instance.station_name)
        fuel_data = validated_data.pop('fuel')

        value = 0
        station = PetrolStation.objects.filter(id=instance.id)

        for fuel in fuel_data:
            fuel_info = fuel['fuel_price_info']
            value = fuel_info['value']

        for state in station:
            fuel = state.fuel.get()
            price = fuel.fuel_price_info
            price.value= value
            price.save()

        instance.save()
        return instance




   