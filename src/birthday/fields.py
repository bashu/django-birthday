from typing import Any

from django.core.exceptions import FieldError
from django.db.models import Model
from django.db.models.fields import DateField
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.signals import pre_save

from . import utils


def handle_pre_save(instance, **kwargs):
    field_obj = instance._meta.birthday_field  # noqa: SLF001

    birthday = getattr(instance, field_obj.name)
    if not birthday:
        return
    setattr(instance, field_obj.doy_name, utils.doy(birthday))


class BirthdayField(DateField):
    def contribute_to_class(
        self,
        cls: type[Model],
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if hasattr(cls._meta, "birthday_field"):
            msg = (
                "django-birthday does not support multiple "
                "BirthdayFields on a single model"
            )
            raise FieldError(msg)
        # django-stubs doesn't know about this attribute: the field adds it itself.
        cls._meta.birthday_field = self  # type: ignore[attr-defined]

        self.doy_name = f"{name}_dayofyear_internal"
        if not hasattr(cls, self.doy_name):
            dayofyear_field = PositiveSmallIntegerField(
                editable=False,
                default=None,
                null=True,
            )
            dayofyear_field.creation_counter = self.creation_counter

            cls.add_to_class(self.doy_name, dayofyear_field)

        super().contribute_to_class(cls, name, *args, **kwargs)

        pre_save.connect(handle_pre_save, sender=cls)
