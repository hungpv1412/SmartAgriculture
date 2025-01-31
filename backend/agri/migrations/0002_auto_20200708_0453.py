# Generated by Django 3.0.6 on 2020-07-08 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agri', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': 'Báo Cáo'},
        ),
        migrations.AddField(
            model_name='device',
            name='safe_time',
            field=models.PositiveIntegerField(default=120, verbose_name='Thời gian an toàn theo '),
        ),
        migrations.AlterField(
            model_name='command',
            name='status',
            field=models.CharField(choices=[('create', 'Khởi tạo'), ('holding', 'Đang thực thi'), ('finish', 'Đã hoàn thành')], max_length=10, verbose_name='Trạng thái'),
        ),
        migrations.AlterField(
            model_name='command',
            name='time_finish',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Thời gian kết thúc'),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(choices=[('pump', 'Máy bơm'), ('light', 'Đèn')], max_length=10, verbose_name='Loại Thiết Bị'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_type',
            field=models.CharField(choices=[('air', 'Cảm biến không khí'), ('ground', 'Cảm biến đất')], max_length=10, verbose_name='Loại cảm biến'),
        ),
    ]
