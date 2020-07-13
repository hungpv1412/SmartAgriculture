from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from agri.models import Device,Farm, Command, Report, Sensor

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'device_name',
            'device_id',
            'device_type',
            'is_active',
            'turn_on_cond',
            'turn_off_cond',
            'safe_time',

        ]

class SensorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sensor
        fields = [
            'sensor_name',
            'sensor_id',
            'sensor_type',
            'location',
            'is_active',
            'device',
        ]

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'device',
            'report_before',
            'report_after',
            'time_start',
            'time_finish',
            'status',
        ]

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id',
            'index',
            'on_created',
            'sensor',
        ]
class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            
        ]