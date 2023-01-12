from django.urls import path
from .views import employees


urlpatterns = [
    path('get_employees/', employees, name='employees')
]
