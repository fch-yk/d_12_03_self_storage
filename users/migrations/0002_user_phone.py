# Generated by Django 4.2 on 2023-04-18 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(default=1, max_length=30, verbose_name="Телефон"),
            preserve_default=False,
        ),
    ]
