from django.shortcuts import get_object_or_404, render, redirect

from storage.models import Order
from .forms import CreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('storage:index')
    template_name = 'users/signup.html'


def profile(request):
    orders = Order.objects.filter(customer=request.user).days_left()

    if request.POST:
        request_data = request.POST

        fullname = request_data["NAME_EDIT"].split()[:2]

        if len(fullname) == 0:
            request.user.first_name = ''
            request.user.last_name = ''
        elif len(fullname) == 1:
            request.user.first_name = fullname[0]
        else:
            request.user.first_name, request.user.last_name = fullname

        request.user.email = request_data["EMAIL_EDIT"]
        request.user.phone = request_data["PHONE_EDIT"]
        request.user.save()
        return redirect("users:profile")

    return render(request, "users/profile.html", {'orders': orders})

