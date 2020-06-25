from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
import unicodedata
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.postgres.fields import JSONField

class AccountManager(BaseUserManager):
    """Quản lý account, hàm khởi tạo account"""

    def create_account(
        self, 
        username, 
        password=None, 
        active=True, 
        staff=False, 
        admin=False, 
        superuser=False):
        
        if not username:
            raise ValueError("Bắt buộc phải có Username")
        if not password:
            raise ValueError("Bắt buộc phải điền password")
        user = self.model(
            username = self.normalize_username(username)
        )
                   
        user.is_active = active
        user.is_admin = admin
        user.is_staff = staff
        user.is_admin = admin
        user.is_superuser = superuser
        user.set_password(password)   
        user.save(using=self._db)
        
        return user

    def create_staff_account(self, username, password=None):
        
        staff = self.create_account(
            username, 
            password = None, 
            staff = True,
            )

        return staff 
    
    def create_admin_account(self, username, password=None):
        
        admin = self.create_account(
            username, 
            password, 
            staff = True, 
            admin = True,
            )
        
        return admin
    

    def create_superuser(self, username, password=None):
        superuser = self.create_account(
            username, 
            password, 
            staff = True, 
            admin = True,
            superuser = True,
            )
        return superuser
    
    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username
# Create your models here.
class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=32, 
        unique=True,
        verbose_name='Username',
        )
    is_active = models.BooleanField(
        default = True,
        verbose_name = 'Trạng thái kích hoạt',
        )
    
    is_staff = models.BooleanField(
        default = False,
        verbose_name = 'Nhân viên',
        )

    is_admin = models.BooleanField(
        default = False,
        verbose_name = 'Nhân viên quản lý',
        )

    is_superuser = models.BooleanField(
        default = False,
        verbose_name = 'Quản lý cao cấp',
        )

    # profile = JSONField(
    #     verbose_name= 'Profile',
    #     default=dict,
    # )
    date_joined = models.DateTimeField(
        auto_now_add = True, 
        null = True,
        verbose_name = 'Ngày thêm',
        )

    last_login = models.DateTimeField(
        auto_now_add = True, 
        null = True, 
        verbose_name = 'Lần đăng nhập cuối',
        )
    
    USERNAME_FIELD = 'username'

    objects = AccountManager()

    @property
    def check_perm(self):
        if self.is_staff:
            if self.is_admin :
                return "admin"
            else :
                return "staff"
        else :
            return "customer"

            
class StaffManager(AccountManager):
    """Quản lý model Nhân viên"""
    
    def get_queryset(self):
        return super(StaffManager, self).get_queryset().filter(is_staff=True)

class Staff(Account):
    
    objects = StaffManager()

    class Meta():
        proxy = True
        managed = True
        verbose_name = 'Nhân Viên'
        verbose_name_plural = 'Danh Sách Nhân viên'
        
class CustomerManager(AccountManager):
    
    """Quản lý tài khoản khách hàng"""
    
    def get_queryset(self):
        return super(CustomerManager, self).get_queryset().filter(is_staff=False)


class Customer(Account):
    """Model Tài khoản khách hàng, kế thừa từ Account"""
    
    objects = CustomerManager()
    
    class Meta:
        proxy = True
        managed = True
        verbose_name = 'Khách Hàng'
        verbose_name_plural = 'Danh Sách Khách Hàng'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('is_staff').default = False
    
