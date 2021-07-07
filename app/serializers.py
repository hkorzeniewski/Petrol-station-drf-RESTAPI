# from app.views import petrol_station_list
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.response import Response
from .models import Fuel, PetrolStation, Price, StationLocation
from django.utils import timezone


class PriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'value', 'change_date', 'user']
    
    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        return instance
    
    def validate(self, attrs):
        if attrs['value'] < 0:
            raise serializers.ValidationError("value cannot be less than 0")
        return attrs


class FuelDetailSerializer(serializers.ModelSerializer):
    fuel_price_info = PriceDetailSerializer()
    class Meta: 
        model = Fuel
        fields = ['id','fuel_type', 'fuel_price_info']
    
    # def to_representation(self, instance):
    #     data = super(FuelDetailSerializer, self).to_representation(instance)
    #     return dict(fuel=data)



class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationLocation
        fields = ['id', 'voivodeship', 'city_name', 'street_name', 'x_coordinate', 'y_coordinate']


class PetrolStationSerializer(serializers.ModelSerializer):
    fuel = FuelDetailSerializer(many=True)

    location = LocationDetailSerializer()
    class Meta:
        model = PetrolStation
        fields = ['id', 'station_name', 'fuel', 'location']


    def create(self, validated_data):

        raw_fuel = validated_data.pop('fuel')
        location_data = validated_data.pop('location')
        raw_name = validated_data.pop('station_name')
        if location_data != '':
            location = StationLocation.objects.filter(voivodeship=location_data['voivodeship'], city_name=location_data['city_name'], street_name=location_data['street_name'].capitalize())
            if not location:
                location = StationLocation.objects.create(voivodeship=location_data['voivodeship'], city_name=location_data['city_name'], street_name=location_data['street_name'].capitalize())  
            else:
                location =  StationLocation.objects.get(voivodeship=location_data['voivodeship'], city_name=location_data['city_name'], street_name=location_data['street_name'].capitalize())  
        petrol_station = PetrolStation.objects.create(station_name=raw_name, location=location)

        for fuel_data in raw_fuel:
            raw = fuel_data.pop('fuel_price_info')
            price = Price.objects.create(value=raw['value'], user=raw['user'])
            fuel = Fuel.objects.create(fuel_type=fuel_data['fuel_type'], fuel_price_info=price)
            petrol_station.fuel.add(fuel)

        return petrol_station


    def update(self, instance, validated_data):
        instance.station_name = validated_data.get('station_name', instance.station_name)
        new_fuel_data = validated_data.pop('fuel')

        users = list()
        values = list()
        types = list()
        station = PetrolStation.objects.filter(id=instance.id)
        print(station)
        
        for new_fuel in new_fuel_data:
            fuel_info = new_fuel['fuel_price_info']
            types.append(new_fuel['fuel_type'])
            values.append(fuel_info['value']) 
            users.append(fuel_info['user'])

        fuels = station[0].fuel.all() 

        i = 0
        for fuel in fuels:
            # print(fuel.fuel_price_info.id)
            for x in types:
                print(x)
                if fuel.fuel_type == x:
                    # price = Price.objects.get(id=fuel.fuel_price_info.id)
                    fuel.fuel_price_info.value = values[i]
                    fuel.fuel_price_info.user = users[i]
                    i+=1
                    fuel.fuel_price_info.save()

        instance.save()
        return instance

    def validate(self, attrs):
        if len(attrs['station_name']) < 2:
            raise serializers.ValidationError("station name cannot be less than 2 characters")
        
        # elif (StationLocation.objects.get(street_name=attrs['location']['street_name'], city_name=attrs['location']['city_name'])):
        #     raise serializers.ValidationError("location exists in database")
        return attrs


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # prices = serializers.PrimaryKeyRelatedField(many=True, queryset=PetrolStation.objects.all())
   
    class Meta:
        model = User
        fields= ['id', 'username']
