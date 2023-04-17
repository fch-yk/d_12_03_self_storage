from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(
        _("Email address"),
        unique=True,
        error_messages={
            "unique": _("This email address is already in use.")
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username
