from django.contrib import admin
from .models import PetrolStation, Fuel, Price, StationLocation
# Register your models here.
admin.site.register(Fuel)
admin.site.register(PetrolStation)
admin.site.register(StationLocation)
admin.site.register(Price)