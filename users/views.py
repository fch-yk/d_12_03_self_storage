from django.shortcuts import get_object_or_404, render

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
    return render(request, 'users/profile.html', context)
