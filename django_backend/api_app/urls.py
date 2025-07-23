from django.urls import path
from .views import SensorDataAPI

urlpatterns = [
    path('sensor-data/', SensorDataAPI.as_view(), name='sensor-data'),
]