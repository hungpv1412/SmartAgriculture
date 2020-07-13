from django.contrib import admin
from .models import Command, Device, Farm, Report, Sensor
# Register your models here.
# admin.site.register(Command)
# admin.site.register(Device)
# admin.site.register(Report)
# admin.site.register(Sensor)
# admin.site.register(Farm)



@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    model = Farm
    list_display = (
        'id',
        'name',
        'device',
        'sensor',
        'farm_map',
        'location',

    )
    
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    model = Device
    list_display = (
        'id',
        'device_name',
        'device_id',
        'device_type',
        'is_active',
        'turn_on_cond',
        'turn_off_cond',
        'safe_time',

    )

    list_display_links = (
        'id',
        'device_name',
        'device_id',
    )

    
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    model = Report
    list_display = (
        'id',
        'on_created',
        'index',
        'sensor__sensor_id',
    )
    list_display_links = (
        'id',
        # 'sensor',
    )
    list_select_related = True
    # def queryset(self, request):
    #     return super(ReportAdmin, self).queryset(request).select_related('sensor')
    def sensor__sensor_id(self, obj):
        return obj.sensor.sensor_id
    sensor__sensor_id.short_description = "Ma cam bien"

@admin.register(Sensor)
class Sensor(admin.ModelAdmin):
    model = Sensor
    list_display = (
        'id',
        'sensor_name',
        'sensor_id',
        'sensor_type',
        'is_active',
        'device',
        )

    list_display_links = ('sensor_name','sensor_id','device')

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    model = Command
    list_display = (
        'device',
        'report_before__index',
        'report_after__index',
        'time_start',
        'time_finish',
        'status',
        )

    def report_before__index(self, obj):
        return obj.report_before.index
    def report_after__index(self, obj):
        return obj.report_after.index