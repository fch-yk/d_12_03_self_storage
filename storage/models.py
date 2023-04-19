import datetime

from django.db import models
from django.db.models import Min, Count, Q

from users.models import User


class StorageQuerySet(models.QuerySet):
    def min_price(self):
        return self.annotate(min_price=Min('boxes__price'))

    def available_boxes(self):
        return self.annotate(
            empty_boxes=Count(
                'boxes',
                filter=Q(boxes__is_available=True),
                distinct=True
            ),
            all_boxes=Count(
                'boxes',
                distinct=True
            )
        )


class Storage(models.Model):
    NEAR_THE_SUBWAY = "NEAR_THE_SUBWAY"
    PARKING = "PARKING"
    HIGH_CEILING = "HIGH_CEILING"
    PROPERTY_CHOICES = [
        (NEAR_THE_SUBWAY, "Рядом с метро"),
        (PARKING, "Парковка"),
        (HIGH_CEILING, "Высокие потолки")
    ]
    city = models.CharField(verbose_name='Город', max_length=100)
    address = models.CharField(verbose_name='Адрес склада', max_length=100)
    description = models.TextField(verbose_name='Описание склада', blank=True)
    temperature = models.SmallIntegerField(verbose_name='Температура на складе', blank=True, null=True)
    max_height = models.DecimalField(verbose_name='Максимальная высота потолка', decimal_places=2, max_digits=5)
    contact = models.TextField(verbose_name='Контакты склада', blank=True)
    route_description = models.TextField(verbose_name='Проезд до склада', blank=True)
    special_property = models.CharField(verbose_name='Свойство склада', choices=PROPERTY_CHOICES, blank=True, max_length=25)

    objects = StorageQuerySet.as_manager()

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.city} - {self.address}'


class Box(models.Model):
    storage = models.ForeignKey(Storage, verbose_name='Склад', related_name='boxes', on_delete=models.CASCADE)
    floor = models.SmallIntegerField(verbose_name='Этаж', blank=True, null=True)
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


class Image(models.Model):
    storage = models.ForeignKey(Storage, verbose_name='Склад', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение', upload_to='imgs/')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.pk} - {self.storage}'
