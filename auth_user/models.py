from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        user = 'user', _('User')
        moderator = 'moderator', _('Moderator')
        admin = 'admin', _('Admin')
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(_('email'), unique=True, db_index=True)
    role = models.CharField(max_length=10,
                            choices=RoleChoices.choices,
                            default=RoleChoices.user)

    @property
    def is_moderator(self):
        return self.role == self.RoleChoices.moderator

    @property
    def is_admin(self):
        return self.role == self.RoleChoices.admin

    @property
    def is_user(self):
        return self.role == self.RoleChoices.user


User = get_user_model()
