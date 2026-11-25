from django.db import models

from birthday import BirthdayField
from birthday import BirthdayManager


class TestModel(models.Model):
    __test__ = False

    birthday = BirthdayField()
    objects = BirthdayManager()

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return str(self.birthday)
