from django.shortcuts import render


def show_home(request):
    context = {}
    template = 'storage/index.html'
    return render(request, template, context=context)
