import datetime
import io
from email.mime.image import MIMEImage

import qrcode
from django.core.mail import EmailMessage

from self_storage import settings

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from storage.models import Storage, Order, Box


def show_home(request):
    context = {}
    template = "storage/index.html"
    return render(request, template, context=context)


def show_faq_page(request):
    context = {}
    template = "storage/faq.html"
    return render(request, template, context=context)


def show_boxes_page(request):
    storages = (
        Storage.objects.prefetch_related("boxes").min_price().available_boxes().all()
    )

    context = {"storages": storages}
    template = "storage/boxes.html"
    return render(request, template, context=context)

@login_required()
def show_payment_page(request, box_id):
    template = "storage/payment.html"

    box = get_object_or_404(Box, id=box_id)
    context = {"box": box}
    if request.POST:
        Order.objects.create(
            customer=request.user,
            box=box,
            is_payment=True,
            price=box.price,
            end_order=datetime.datetime.now() + datetime.timedelta(days=30)
        )
        box.is_available = False
        box.save()

        return redirect("users:profile", request.user.username)

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
