import datetime

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
