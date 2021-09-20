from django.db import models

import birthday


class TestModel(models.Model):
    birthday = birthday.fields.BirthdayField()
    objects = birthday.managers.BirthdayManager()

    class Meta:
        ordering = ('pk',)
