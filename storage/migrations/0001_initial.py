# Generated by Django 4.2 on 2023-04-18 08:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Box",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.CharField(max_length=25, verbose_name="Номер бокса")),
                ("width", models.FloatField(verbose_name="ширина")),
                ("length", models.FloatField(verbose_name="длина")),
                ("height", models.FloatField(verbose_name="высота")),
                (
                    "is_available",
                    models.BooleanField(default=True, verbose_name="Свободен"),
                ),
                ("price", models.PositiveSmallIntegerField(verbose_name="Стоимость")),
            ],
            options={
                "verbose_name": "Бокс",
                "verbose_name_plural": "Боксы",
            },
        ),
        migrations.CreateModel(
            name="Storage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=100, verbose_name="Город")),
                (
                    "address",
                    models.CharField(max_length=100, verbose_name="Адрес склада"),
                ),
            ],
            options={
                "verbose_name": "Склад",
                "verbose_name_plural": "Склады",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_order",
                    models.DateField(
                        default=datetime.datetime.now, verbose_name="Начало аренды"
                    ),
                ),
                ("end_order", models.DateField(verbose_name="Конец аренды")),
                ("is_payment", models.BooleanField(verbose_name="Оплачен")),
                (
                    "need_delivery",
                    models.BooleanField(verbose_name="Требуется доставка"),
                ),
                (
                    "need_measurements",
                    models.BooleanField(verbose_name="Требуется замер"),
                ),
                ("price", models.PositiveSmallIntegerField(verbose_name="Стоимость")),
                (
                    "box",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="orders",
                        to="storage.box",
                        verbose_name="Бокс",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Заказчик",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
            },
        ),
        migrations.AddField(
            model_name="box",
            name="storage",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="boxes",
                to="storage.storage",
                verbose_name="Склад",
            ),
        ),
    ]