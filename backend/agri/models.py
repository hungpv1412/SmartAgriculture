from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Device(models.Model):
    """Thiết bị trong nông trại"""
    device_name = models.CharField(
        verbose_name="Tên Thiết bị",
        max_length=255,
    )
    device_id = models.CharField(
        verbose_name="Mã Thiết bị",
        max_length=10,
        unique=True,
    )
    device_type = models.CharField(
        verbose_name="Loại Thiết Bị",
        max_length=10,
        choices=[
            ('pump','Máy bơm'),
            ('light','Đèn')
        ],
        blank=False,
        null=False,
    )
    is_active = models.BooleanField(
        verbose_name="Trạng thái",
        default=False,
        blank=False,
        null=False,
    )
    turn_on_cond = models.FloatField(
        verbose_name="Điều kiện khởi động",
    )
    turn_off_cond = models.FloatField(
        verbose_name="Điều kiện tắt",
    )
    safe_time = models.PositiveIntegerField(
        verbose_name="Thời gian an toàn theo ",
        default=120,
        null=False,
        blank=False,
    )
    def __str__(self):
        return self.device_name

    

class Sensor(models.Model):
    """Cảm biến"""
    sensor_name = models.CharField(
        verbose_name="tên cảm biến",
        max_length=255,
        blank=False,
        null=False,
    )

    sensor_id = models.CharField(
        verbose_name="Mã Cảm biến",
        max_length=10,
        blank=False,
        null=False,
        unique=True,
    )

    sensor_type = models.CharField(
        verbose_name="Loại cảm biến",
        max_length=10,
        choices = [
            ('air','Cảm biến không khí'),
            ('ground','Cảm biến đất')
        ],
        blank=False,
        null=False,
    )
    location = models.CharField(
        verbose_name="Vị trí",
        max_length=127,
        null=False,
        blank=False,
    )
    is_active = models.BooleanField(
        verbose_name="Trạng thái",
        default=False,
        blank=False,
        null=False,
    )
    device = models.ForeignKey(
        verbose_name="thiết bị liên kết",
        to=Device,
        to_field="id",
        on_delete=models.DO_NOTHING,
    )
    def __str__(self):
        return self.sensor_name


class Report(models.Model):
    """Báo cáo từ Cảm biến"""
    index = JSONField(
        verbose_name="thông số",
        null=False,
        blank=False,
        editable=False,

    )
    # index = models.TextField(
    #     verbose_name="thông số",
    #     null=False,
    #     blank=False,
    #     editable=False,

    # )
    on_created = models.DateTimeField(
        verbose_name="Thời gian report",
        auto_now_add=True,

    )
    sensor = models.ForeignKey(
        verbose_name="Cảm biến report",
        to=Sensor,
        to_field="id",
        on_delete=models.DO_NOTHING,
    )
    class Meta():
        verbose_name="Báo Cáo"
    def __str__(self):
        return self.sensor.sensor_name+" "+str(self.on_created)


class Command(models.Model):
    """Lệnh điều khiển thiết bị và kết quả"""
    device = models.ForeignKey(
        verbose_name="Thiết bị điều khiển",
        to=Device,
        to_field="device_id",
        on_delete=models.DO_NOTHING,
    )
    report_before = models.ForeignKey(
        verbose_name="thông số trước điều khiển",
        to=Report,
        to_field="id",
        on_delete=models.DO_NOTHING,
        related_name="report_before"
    )
    report_after = models.ForeignKey(
        verbose_name="thông số sau điều khiển",
        to=Report,
        to_field="id",
        on_delete=models.DO_NOTHING,
        related_name="report_after",
        
    )
    time_start = models.DateTimeField(
        verbose_name="Thời gian bắt đầu",
        auto_now_add=True,
    )
    time_finish = models.DateTimeField(
        verbose_name="Thời gian kết thúc",
        blank=True,
        null=True,   
    )
    status = models.CharField(
        verbose_name="Trạng thái",
        max_length=10,
        choices=[
            ('create', "Khởi tạo"),
            ('holding', "Đang thực thi"),
            ('finish', "Đã hoàn thành"),
        ]
    )
    # @classmethod
    # def create(cls, device, report_before, status):
    #     command= cls(
    #         device=device,
    #         report_before=report_before,
    #         status=status
    #     )
    #     # do something with the book
    #     return command


class Farm(models.Model):
    """Nông trại"""
    name = models.CharField(
        verbose_name="Tên nông trại",
        max_length=100,
        null=False,
        blank=False,
    )

    device = models.ForeignKey(
        to=Device,
        on_delete=models.DO_NOTHING,
        to_field="id",
        db_constraint=True,
    )

    sensor = models.ForeignKey(
        to=Sensor,
        on_delete=models.DO_NOTHING,
        to_field="id",
        db_constraint=True,
    )
    farm_map = models.TextField(
        verbose_name="Bản đồ trang trại",
        blank=False,

    )
    location = models.CharField(
        verbose_name="Vị trí trang trại",
        max_length=127,
    )
