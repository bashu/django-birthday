from django.db import models

from birthday import BirthdayField, BirthdayManager


class TestModel(models.Model):
    birthday = BirthdayField()
    objects = BirthdayManager()

    class Meta:
        ordering = ('pk',)
