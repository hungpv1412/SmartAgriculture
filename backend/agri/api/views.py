from agri.models import (
    Device,
    Sensor,
    Report,
    Command,
    Farm,
)
from .serializers import (
    DeviceSerializer,
    SensorSerializer,
    ReportSerializer,
    CommandSerializer,
    FarmSerializer,
)

from rest_framework import (
    generics,
    viewsets,
    mixins,
    views,
    )

from rest_framework.permissions import IsAuthenticated
from src.api.permissons import (
    IsAdminAuthentication,
    IsStaffAuthentication,
)
#token import
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class DeviceViewset(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ):

    permission_classes = (
        IsAuthenticated,
        IsAdminAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )
    
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class SensorViewset(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ):

    permission_classes = (
        IsAuthenticated,
        IsAdminAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )
    
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class ReportViewset(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ):

    permission_classes = (
        IsAuthenticated,
        IsAdminAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )
    
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class CommandViewset(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ):

    permission_classes = (
        IsAuthenticated,
        IsAdminAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )
    
    queryset = Command.objects.all()
    serializer_class = CommandSerializer