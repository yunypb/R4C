from django.urls import path

from robots.views import export_to_excel

urlpatterns = [
    path('export_to_excel/', export_to_excel, name='export_to_excel')
]