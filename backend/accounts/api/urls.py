from accounts.api.views import (
    CustomerViewSet, 
    StaffViewSet, 
    CreateCustomerView,
    CreateStaffView,
    ChangePasswordCustomerView,
    ChangePasswordStaffView,
    TokenAPI,
    CustomerDetail,
    )
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'customer', CustomerViewSet, basename='Customer View Set')
router.register(r'staff', StaffViewSet, basename='Staff View Set')
# Create a router and register our viewsets with it.
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    
    path(
        'token', 
        TokenAPI.as_view(), 
        name = 'get Token',),

    path(
        'staff/create', 
        CreateStaffView.as_view(), 
        name = 'Create Staff View'),
    
    path(
        'customer/create', 
        CreateCustomerView.as_view(), 
        name = 'Create Customer View'),
    
    path(
        'customer/<pk>/password_change', 
        ChangePasswordCustomerView.as_view(), 
        name = 'Change Customer Password'),
    
    path(
        'staff/<pk>/password_change', 
        ChangePasswordStaffView.as_view(), 
        name = "Change Staff Password"),
    path(
        'profile',
        CustomerDetail.as_view(), 
        name='Customer Profile',),
]

