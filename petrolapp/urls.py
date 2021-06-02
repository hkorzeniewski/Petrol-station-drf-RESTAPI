"""petrolapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app.models import PetrolStation
from django.contrib import admin
from django.db import router
from django.urls import path, include, re_path
from rest_framework import routers
from app import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.api_root),
    path('stations/', views.PetrolStationList.as_view(), name='station-list'),
    path('stations/<int:pk>', views.PetrolStationDetail.as_view()),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/',  views.CustomAuthToken.as_view()),
    path('admin/', admin.site.urls)
]
