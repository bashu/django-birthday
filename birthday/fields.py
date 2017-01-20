# -*- coding: utf-8 -*-

from django.core.exceptions import FieldError
from django.db.models.fields import DateField, PositiveSmallIntegerField
from django.db.models.signals import pre_save

internal_field = PositiveSmallIntegerField(editable=False, default=None, null=True)


def pre_save_listener(instance, **kwargs):
    field = instance._meta.birthday_field
    birthday = getattr(instance, field.name)
    if not birthday:
        return
    setattr(instance, field.doy_name, birthday.timetuple().tm_yday)


class BirthdayField(DateField):        

    def contribute_to_class(self, cls, name):
        super(BirthdayField, self).contribute_to_class(cls, name)

        if hasattr(cls._meta, 'birthday_field'):
            raise FieldError("django-birthday does not support multiple BirthdayFields on a single model")

        cls._meta.birthday_field = self

        self.doy_name = '%s_dayofyear_internal' % name
        internal_field.contribute_to_class(cls, self.doy_name)

        pre_save.connect(pre_save_listener, sender=cls)
