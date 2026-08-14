from django.core.exceptions import FieldError
from django.db.models.fields import DateField
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.signals import pre_save


def handle_pre_save(instance, **kwargs):
    field_obj = instance._meta.birthday_field  # noqa: SLF001

    birthday = getattr(instance, field_obj.name)
    if not birthday:
        return
    setattr(instance, field_obj.doy_name, birthday.timetuple().tm_yday)


class BirthdayField(DateField):
    def contribute_to_class(self, cls, name):
        if hasattr(cls._meta, "birthday_field"):
            msg = (
                "django-birthday does not support multiple "
                "BirthdayFields on a single model"
            )
            raise FieldError(msg)
        cls._meta.birthday_field = self

        self.doy_name = f"{name}_dayofyear_internal"
        if not hasattr(cls, self.doy_name):
            dayofyear_field = PositiveSmallIntegerField(
                editable=False,
                default=None,
                null=True,
            )
            dayofyear_field.creation_counter = self.creation_counter

            cls.add_to_class(self.doy_name, dayofyear_field)

        super().contribute_to_class(cls, name)

        pre_save.connect(handle_pre_save, sender=cls)
