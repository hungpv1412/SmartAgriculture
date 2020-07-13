from agri.api.views import (
    DeviceViewset,
    ReportViewset,
    CommandViewset,
    SensorViewset,
)

from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'device', DeviceViewset, basename='Device Viewset')
router.register(r'sensor', SensorViewset, basename='Sensor Viewset')
router.register(r'report', ReportViewset, basename='Report Viewset')
router.register(r'command',CommandViewset, basename='Command Viewset')
# Create a router and register our viewsets with it.
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    
]

