from django.contrib import admin
from .models import Command, Device, Farm, Report, Sensor
# Register your models here.
admin.site.register(Command)
admin.site.register(Device)
admin.site.register(Report)
admin.site.register(Sensor)
admin.site.register(Farm)
