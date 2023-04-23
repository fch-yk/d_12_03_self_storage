import requests
from django.conf import settings
from django.db import models


class Location(models.Model):
    address = models.CharField(
        verbose_name='адрес',
        max_length=150,
        unique=True,
    )

    latitude = models.FloatField(verbose_name='широта',)
    longitude = models.FloatField(verbose_name='долгота',)
    changed_at = models.DateTimeField(
        verbose_name='изменена в',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self):
        return f'Локация № {self.id} {self.address}'

    @classmethod
    def save_location(cls, address):
        coordinates = cls.fetch_coordinates(
            settings.YA_API_KEY,
            address
        )
        if coordinates:
            latitude, longitude = coordinates
            cls.objects.update_or_create(
                address=address,
                defaults={'latitude': latitude, 'longitude': longitude}
            )

    @staticmethod
    def fetch_coordinates(apikey, address):
        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(base_url,
                                params={
                                    "geocode": address,
                                    "apikey": apikey,
                                    "format": "json",
                                })
        response.raise_for_status()
        found_response = response.json()['response']
        found_places = found_response['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lat, lon
