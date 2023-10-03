from django.contrib import admin
from django.urls import path

from robots.views import model_create

urlpatterns = [
    path('create',model_create),
]
