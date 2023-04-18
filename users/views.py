from django.shortcuts import get_object_or_404, render, redirect

from .forms import CreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('storage:index')
    template_name = 'users/signup.html'

def profile(request, username):
    current_user = get_object_or_404(User, username=username)
    context = {
        'current_user': current_user,
    }

    if request.POST:
        request_data = request.POST

        if request_data["PASSWORD_EDIT"] == '':
            raise Exception('Пароль не может быть пустым!')

        fullname = request_data["NAME_EDIT"].split()[:2]

        current_user.first_name = ''
        current_user.last_name = ''

        if len(fullname) == 1:
            current_user.first_name = fullname[0]
        else:
            current_user.first_name, current_user.last_name = fullname

        current_user.email = request_data["EMAIL_EDIT"]
        current_user.phone = request_data["PHONE_EDIT"]
        current_user.set_password(request_data["PASSWORD_EDIT"])
        current_user.save()
        return redirect("users:login")


    return render(request, "users/profile.html", context)

