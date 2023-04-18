
from .forms import CreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('storage:index')
    template_name = 'users/signup.html'
from django.shortcuts import render
