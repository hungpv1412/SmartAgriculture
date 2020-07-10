from accounts.models import Staff, Customer, Account

from .serializers import (
    CustomerSerializer, 
    StaffSerializer,
    CustomerCreateSerializer,
    StaffCreateSerializer,
    CustomerPasswordChangeSerializer,
    StaffPasswordChangeSerializer,
    )
from rest_framework import (
    generics,
    viewsets,
    mixins,
    views,
    )
from rest_framework.response import Response

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

class TokenAPI(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key , 'status':'1',"perm":token.user.check_perm },)
        else :
            return Response({"token": "Error", "status":"0"},)

class StaffViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    ):
    
    permission_classes = (
        IsAuthenticated,
        IsAdminAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )
    
    queryset = Staff.objects.filter(is_staff=True)
    serializer_class = StaffSerializer

class CustomerViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,):
    
    permission_classes = (
        IsAuthenticated,
        IsStaffAuthentication,)
    
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,)

    queryset = Customer.objects.filter(is_staff=False)
    serializer_class = CustomerSerializer

class CreateCustomerView(generics.CreateAPIView):
    permission_classes = (
        IsAuthenticated,
        IsStaffAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )

    queryset = Customer.objects.filter(is_staff=False)
    serializer_class = CustomerCreateSerializer

class ChangePasswordCustomerView(generics.RetrieveUpdateAPIView):

    permission_classes = (
        IsAuthenticated,
        IsStaffAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )

    queryset = Customer.objects.filter(is_staff=False)
    serializer_class = CustomerPasswordChangeSerializer

class CreateStaffView(generics.CreateAPIView):
    permission_classes = (
        IsAuthenticated,
        IsAdminAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )

    queryset = Staff.objects.filter(is_staff=True)
    serializer_class =StaffCreateSerializer

class ChangePasswordStaffView(generics.RetrieveUpdateAPIView):

    permission_classes = (
        IsAuthenticated,
        IsAdminAuthentication,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )

    queryset = Staff.objects.filter(is_staff=True)
    
    serializer_class = StaffPasswordChangeSerializer

class CustomerDetail(views.APIView):
    permission_classes = (
        IsAuthenticated,
        )
    authentication_classes = (
        TokenAuthentication, 
        SessionAuthentication,
        )
    
    def get(self, request):
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data)

