from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext, gettext_lazy as _

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(_('email'), unique=True)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
