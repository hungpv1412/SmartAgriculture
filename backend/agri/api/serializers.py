from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from agri.models import Device,Farm, Command, Report, Sensor

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [

        ]

class SensorSerializer(serializers.ModelSerializer):
    model=Sensor
    class Meta:
        fields = [
            
        ]

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            
        ]

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            
        ]
class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            
        ]