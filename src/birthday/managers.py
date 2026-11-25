from django.db import models
from django.db.models import Case
from django.db.models import F
from django.db.models import When
from django.db.models.query_utils import Q
from django.utils import timezone

from . import utils

# maximum possible canonical day-of-year value (Dec 31 in the reference
# leap year) -- must stay in sync with birthday.utils.doy's range.
YEAR = 366


def _order(manager, *, reverse=False, case=False):
    cdoy = utils.doy(timezone.localdate())
    bdoy = manager._birthday_doy_field  # noqa: SLF001
    if case:
        qs = manager.annotate(
            internal_bday_order=Case(
                When(**{f"{bdoy}__lt": cdoy}, then=F(bdoy) + YEAR),
                default=F(bdoy),
                output_field=models.IntegerField(),
            ),
        )
        order_field = "internal_bday_order"
    else:
        qs = manager.all()
        order_field = bdoy
    if reverse:
        return qs.order_by(f"-{order_field}")
    return qs.order_by(order_field)


class BirthdayManager(models.Manager):
    @property
    def _birthday_doy_field(self):
        return self.model._meta.birthday_field.doy_name  # noqa: SLF001

    def _doy(self, day):
        if not day:
            day = timezone.localdate()
        return utils.doy(day)

    def get_upcoming_birthdays(
        self,
        days=30,
        after=None,
        *,
        include_day=True,
        order=True,
        reverse=False,
    ):
        today = self._doy(after)
        limit = today + days
        q = Q(
            **{
                "{}__gt{}".format(
                    self._birthday_doy_field,
                    "e" if include_day else "",
                ): today,
            },
        )
        q &= Q(**{f"{self._birthday_doy_field}__lt": limit})

        if limit > YEAR:
            limit = limit - YEAR
            today = 1
            q2 = Q(**{f"{self._birthday_doy_field}__gte": today})
            q2 &= Q(**{f"{self._birthday_doy_field}__lt": limit})
            q = q | q2

        if order:
            qs = _order(self, reverse=reverse, case=True)
            return qs.filter(q)

        return self.filter(q)

    def get_birthdays(self, day=None):
        return self.filter(**{self._birthday_doy_field: self._doy(day)})

    def order_by_birthday(self, *, reverse=False):
        return _order(self, reverse=reverse)
