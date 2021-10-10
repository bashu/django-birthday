from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from birthday import BirthdayField, BirthdayManager

class CustomUserManager(BaseUserManager, BirthdayManager):
    pass

class CustomUser(AbstractUser):
    birthday = BirthdayField(null=True, blank=True)

    objects = CustomUserManager()
