from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from storage.models import Order
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('storage:index')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid


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
