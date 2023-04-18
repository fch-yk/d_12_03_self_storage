import datetime

from django.db import models

from users.models import User


class Storage(models.Model):
    city = models.CharField(verbose_name='Город', max_length=100)
    address = models.CharField(verbose_name='Адрес склада', max_length=100)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.city} - {self.address}'


class Box(models.Model):
    storage = models.ForeignKey(Storage, verbose_name='Склад', related_name='boxes', on_delete=models.CASCADE)
    number = models.CharField(verbose_name='Номер бокса', max_length=25)
    width = models.FloatField('ширина')
    length = models.FloatField('длина')
    height = models.FloatField('высота')
    is_available = models.BooleanField(verbose_name='Свободен', default=True)
    price = models.PositiveSmallIntegerField(verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'{self.number} - {self.is_available}'


class Order (models.Model):
    customer = models.ForeignKey(User, verbose_name='Заказчик', related_name='orders', on_delete=models.CASCADE)
    box = models.ForeignKey(Box, verbose_name='Бокс', related_name='orders', on_delete=models.DO_NOTHING)
    start_order = models.DateField(verbose_name='Начало аренды', default=datetime.datetime.now)
    end_order = models.DateField(verbose_name='Конец аренды')
    is_payment = models.BooleanField(verbose_name='Оплачен')
    need_delivery = models.BooleanField(verbose_name='Требуется доставка')
    need_measurements = models.BooleanField(verbose_name='Требуется замер')
    price = models.PositiveSmallIntegerField(verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.pk} - {self.customer}'
