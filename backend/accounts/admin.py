from django.contrib import admin
from .models import Customer, Staff
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
# from .forms import (
#     CustomerChangeForm, 
#     CustomerCreationForm,
#     StaffChangeForm,
#     StaffCreationForm,
#     )
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, 
    UserChangeForm, 
    UserCreationForm,
)

from django.utils.translation import gettext, gettext_lazy as _

from django.utils.html import format_html
   

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    change_user_password_template = None
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # (_('Personal info'), {'fields': ('full_name',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('last_login','date_joined',)
    # form = CustomerChangeForm
    # add_form = CustomerCreationForm
    # change_password_form = AdminPasswordChangeForm
    list_display = ('id','username', 'last_login' )
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions',)


    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(is_staff=False)
        return qs

@admin.register(Staff)
class StaffAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name','birthday')}),
        # (_('Customer Profile'),{'inlines',('CustomerProfileInline',)}),
        (_('Permissions'), {'fields': ('is_active','is_admin'),}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_admin'),
        }),
    )
    readonly_fields = ('last_login','date_joined',)
    # form = StaffChangeForm
    # add_form = StaffCreationForm
    # change_password_form = AdminPasswordChangeForm
    list_display = ('id','username')
    ordering = ('id',)

    

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(is_staff=True)
        return qs
