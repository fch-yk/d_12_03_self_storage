from django.shortcuts import render


def show_home(request):
    context = {}
    return render(request, 'index.html', context=context)
