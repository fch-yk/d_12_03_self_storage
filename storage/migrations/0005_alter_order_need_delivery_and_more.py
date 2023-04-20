# Generated by Django 4.0.10 on 2023-04-20 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_box_floor_storage_max_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='need_delivery',
            field=models.BooleanField(default=False, verbose_name='Требуется доставка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='need_measurements',
            field=models.BooleanField(default=False, verbose_name='Требуется замер'),
        ),
    ]