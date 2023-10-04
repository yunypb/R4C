from django.contrib import admin
from django.urls import path, include

from robots.views import notify_client

urlpatterns = [
    path('email', notify_client),
]
