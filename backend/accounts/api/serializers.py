from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Customer, Staff
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ProfileSerializer(serializers.Serializer):
    
    class Meta:

        fields = [   
   
            'address',
        ]
    # def create(self, validated_data):
    #     meter_id = validated_data.pop('meter')
        
    #     customerprofile = CustomerProfile(
    #         address = validated_data.get('address'),
    #         person_num = validated_data.get('person_num'),
    #         customer_type = validated_data.get('customer_type'),
    #     )
    #     meter = Meter.objects.get(pid_number=meter_id)
    #     customerprofile.meter= meter
    #     customerprofile.save()
    #     return customerprofile
    # def update(self, instance, validated_data):
    #     meter = validated_data.pop('meter')
    #     customerprofile = CustomerProfile.objects.get_or_create(**validated_data)
    #     # instance.address = validated_data.get('address')
    #     # instance.person_num = validated_data.get('person_num')
    #     # instance.customer_type = validated_data.get('customer_type')
    #     # instance.meter(meter)
    #     instance.save()
        
    #     return instance

class CustomerSerializer(WritableNestedModelSerializer):
    customerprofile = ProfileSerializer()
    
    class Meta:
        model = Customer
        fields = [
            'id',
            'username',
            'full_name',
            'birthday',
            'is_active',
            'date_joined',
            'last_login',
            'customerprofile',
        ]
        read_only_fields = [
            'id',
        ]


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
            'id',
            'username',
            'full_name',
            'birthday',
            'is_active',
            'is_staff',
            'is_admin',
            'date_joined',
            'last_login',
        ]
        read_only_fields = [
            'id',
            'is_staff',
        ]

class CustomerCreateSerializer(WritableNestedModelSerializer):
    
    customerprofile = ProfileSerializer()
    
    re_password = serializers.CharField(
        style = {'input_type' : 'password'},
        write_only=True,
        required = True,
        )
    
    password = serializers.CharField(
        style = {'input_type' : 'password'},
        write_only = True,
        required = True,
        )
    
    class Meta:
        model = Customer
        fields = [
            'id',
            'username',
            'password',
            're_password',
            'is_active',
            'full_name',
            'birthday',
            'customerprofile',
        ]
       
    def create(self, validated_data):
        
        profile_validated_data = validated_data.pop('customerprofile')
        
        password = validated_data.pop('password')
        
        re_password = validated_data.pop('re_password')
        
        customer = Customer.objects.create(**validated_data)

        if password!=re_password:
            raise serializers.ValidationError({"password":"password not match"})
        customer.set_password(password)
        customer.save()
        
        customerprofile_serializer = ProfileSerializer()
        profile_validated_data['customer'] = customer
        customerprofile =  customerprofile_serializer.create(profile_validated_data)
        
        return customer
    
    # def update(self, instance, validated_data):
    #     # Handle related objects
    #     print("start update")
    #     customerprofile_data = validated_data.pop('customerprofile')
    #     customerprofile_serializer = self.fields['customerproflie']
    #     customerprofile = instance.customerproflie
        
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.full_name = validated_data.get('full_name', instance.full_name)
    #     instance.birthday = validated_data.get('birthday', instance.birthday)
        
    #     if password!=password2:
    #         raise serializers.ValidationError({"password":"password not match"})
        
    #     instance.set_password(validated_data.get('password', instance.password))
    #     instance.save()

    #     customerprofile.address = customerprofile_data.get('address', customerprofile.address)
    #     customerprofile.person_num = customerprofile_data.get('person_num', customerprofile.person_num)
    #     customerprofile.customer_type = customerprofile_data.get('customer_type', customerprofile.customer_type)
    #     customerprofile.save()
        
    #     return instance

class StaffCreateSerializer(serializers.ModelSerializer):
    
    re_password = serializers.CharField(
        style = {'input_type' : 'password'},
        write_only = True,
        required = True,
        )
    password = serializers.CharField(
        style = {'input_type' : 'password'},
        write_only = True,
        required = True,
        )

    class Meta:
        model = Staff
        fields = [
            # 'id',
            'username',
            'password',
            're_password',
            'full_name',
            'birthday',
            'is_admin',
        ]
    
    def create(self, validated_data):
        staff = Staff(
            username = validated_data['username'],
            full_name = validated_data['full_name'],
            birthday = validated_data['birthday'],
            is_admin = validated_data['is_admin'],
            is_staff = True,
        )
        password = validated_data['password']
        re_password = validated_data['re_password']

        if password!=re_password:
            raise serializers.ValidationError({"password":"password not match"})
        staff.set_password(password)
        staff.save()
        return staff

class CustomerPasswordChangeSerializer(serializers.ModelSerializer):
    """Đổi mật khẩu tài khoản khách hàng dành cho Staff"""
    
    re_password = serializers.CharField(
        style = {'input_type' : 'password'},
        write_only=True,
        required = True,
        )
    
    password = serializers.CharField(
        style = {'input_type' : 'password'},
        write_only=True,
        required = True,
        )

    class Meta():
        model = Customer
        fields = [
            'id',
            'password',
            're_password',
        ]
    
    def update(self, instance, validated_data):  
        
        password = validated_data['password']
        re_password = validated_data['re_password']

        if password!=re_password:
            raise serializers.ValidationError({"password":"password not match"})
        else:
            instance.set_password(password)
            instance.save()
        
        return instance
        

class StaffPasswordChangeSerializer(serializers.ModelSerializer):
    """Đổi mật khẩu tài khoản nhân viên"""
    
    re_password = serializers.CharField(
        style = {'input_type' : 'password'},
        write_only=True,
        required = True,
        )
    
    password = serializers.CharField(
        style = {'input_type' : 'password'},
        write_only = True,
        required = True,
        )

    class Meta():
        model = Staff
        fields = [
            'id',
            'password',
            're_password',
        ]
    
    def update(self, instance, validated_data):  
        
        password = validated_data['password']
        re_password = validated_data['re_password']

        if password!=re_password:
            raise serializers.ValidationError({"password":"password not match"})
        else:
            instance.set_password(password)
            instance.save()
        
        

        return instance