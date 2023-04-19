from django.shortcuts import render

from storage.models import Storage


def show_home(request):
    context = {}
    template = 'storage/index.html'
    return render(request, template, context=context)


def show_faq_page(request):
    context = {}
    template = 'storage/faq.html'
    return render(request, template, context=context)


def show_boxes_page(request):
    storages = Storage.objects.min_price().available_boxes().all()
    context = {'storages': storages}
    template = 'storage/boxes.html'
    return render(request, template, context=context)
