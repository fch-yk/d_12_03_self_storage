import datetime
import io
import json
import sys
import uuid
from email.mime.image import MIMEImage


import qrcode
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from geopy.distance import distance
from geopy.geocoders import Nominatim
from yookassa import Configuration, Payment

from geo.models import Location
from self_storage import settings
from self_storage.settings import API_KEY, SHOP_ID, RETURN_URL
from storage.models import Box, Order, Storage


def show_home(request):
    context = {}
    template = "storage/index.html"
    return render(request, template, context=context)


def show_faq_page(request):
    context = {}
    template = "storage/faq.html"
    return render(request, template, context=context)


def get_storage_distance(storage):
    return storage.distance


def show_boxes_page(request):
    storages = (
        Storage.objects.prefetch_related(
            "boxes"
        ).prefetch_related('images').min_price().available_boxes().all()
    )

    show_distances = False
    client_address = ''
    for storage in storages:
        storage.nearest = False

    if storages and 'latitude' in request.GET and 'longitude' in request.GET:
        show_distances = True
        client_latitude = float(request.GET['latitude'])
        client_longitude = float(request.GET['longitude'])
        geolocator = Nominatim(user_agent="d_12_03_self_storage")
        client_address = geolocator.reverse(
            (client_latitude, client_longitude)
        ).address

        addresses = set()
        for storage in storages:
            addresses.add(storage.address)

        locations_catalog = {}
        locations = Location.objects.filter(address__in=addresses).values(
            'address',
            'latitude',
            'longitude',
        )
        for location in locations:
            locations_catalog[location['address']] = {
                'latitude': location['latitude'],
                'longitude': location['longitude'],
            }

        for storage in storages:
            storage.distance_error = False
            storage_location = locations_catalog.get(storage.address, None)
            if not storage_location:
                storage.distance_error = True
                storage.distance = sys.maxsize
                continue

            storage.distance = distance(
                (client_latitude, client_longitude),
                (storage_location['latitude'], storage_location['longitude'])
            ).km

        if not all(storage.distance_error for storage in storages):
            nearest_storage = min(storages, key=get_storage_distance)
            nearest_storage.nearest = True

    context = {
        "storages": storages,
        'show_distances': show_distances,
        'client_address': client_address
    }
    template = "storage/boxes.html"
    return render(request, template, context=context)


@login_required()
def show_payment_page(request, box_id):
    template = "storage/payment.html"

    box = get_object_or_404(Box, id=box_id)
    order = Order.objects.create(
        customer=request.user,
        box=box,
        is_payment=False,
        price=box.price,
        end_order=datetime.datetime.now() + datetime.timedelta(days=30)
    )
    box.is_available = False
    box.save()
    context = {"order": order}

    return render(request, template, context)


def make_qr_code(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(pk=order_id)
        order_info = f'''
            Адрес склада: {order.box.storage.address}
            Номер бокса: {order.box.number}
            Срок аренды: {order.start_order} - {order.end_order}
        '''
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(order_info)
        qr_code = qr.make_image(fill_color="black", back_color="white")
        qr_bytes = io.BytesIO()
        qr_code.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)
        image = MIMEImage(qr_bytes.read())
        email = EmailMessage(
            'Your QR',
            'Your QR-code in attachments',
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )
        email.attach(image)
        email.send()
    return redirect("users:profile", request.user.username)


def make_payment(request, order_id):
    if request.method == "GET":
        Configuration.account_id = SHOP_ID
        Configuration.secret_key = API_KEY

        price = Order.objects.get(id=order_id).price
        payment = Payment.create({
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": RETURN_URL
            },
            "capture": True,
            "description": order_id
        }, uuid.uuid4())

        order = Order.objects.get(id=order_id)
        order.payment_id = payment.id
        order.save()

        confirmation_url = payment.confirmation.confirmation_url
        return redirect(confirmation_url)

@csrf_exempt
def update_payment_status(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['object']['status'] == 'succeeded':
            payment_id = body['object']['id']
            order = Order.objects.get(payment_id=payment_id)
            order.is_payment = True
            order.save()
    return HttpResponse(status=200)





