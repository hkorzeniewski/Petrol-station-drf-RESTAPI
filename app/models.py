from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Price(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    change_date = models.DateTimeField(auto_now_add=True)


class Fuel(models.Model):
    FUEL_TYPES = (
        ('P95', 'Petrol P95'),
        ('P98', 'Petrol P98'),
        ('ON', 'Diesel')
    )
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPES)
    fuel_price_info = models.ForeignKey(Price, on_delete=models.CASCADE)


class StationLocation(models.Model):
    VOIVODESHIP_NAMES = (
        ('dolnoslaskie', 'dolnoslaskie'),
        ('kujawsko-pomorskie', 'kujawsko-pomorskie'),
        ('lubelskie', 'lubelskie'),
        ('lubuskie', 'lubuskie'),
        ('lodzkie', 'lodzkie'),
        ('malopolskie', 'malopolskie'),
        ('mazowieckie', 'mazowieckie')
    )
    voivodeship = models.CharField(max_length=30, choices=VOIVODESHIP_NAMES)
    city_name = models.CharField(max_length=20)
    street_name = models.CharField(max_length=30, default="zielona 8", blank=True)
    x_coordinate = models.FloatField(default=1, blank=True)
    y_coordinate = models.FloatField(default=1, blank=True)


class PetrolStation(models.Model):
    station_name = models.CharField(max_length=30)
    fuel = models.ManyToManyField(Fuel)
    location = models.ManyToManyField(StationLocation)

