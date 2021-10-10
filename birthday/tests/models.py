from django.db import models

from birthday import BirthdayField, BirthdayManager


class TestModel(models.Model):
    __test__ = False

    birthday = BirthdayField()
    objects = BirthdayManager()

    class Meta:
        ordering = ("pk",)
