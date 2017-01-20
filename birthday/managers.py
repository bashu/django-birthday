# -*- coding: utf-8 -*-

from datetime import date

from django.db import models
from django.db.models.query_utils import Q

from .fields import BirthdayField

CASE = "CASE WHEN %(bdoy)s<%(cdoy)s THEN %(bdoy)s+365 ELSE %(bdoy)s END"


def _order(manager, reverse=False, case=False):
    cdoy = date.today().timetuple().tm_yday
    bdoy = manager._birthday_doy_field
    doys = {'cdoy': cdoy, 'bdoy': bdoy}
    if case:
        qs = manager.extra(select={'internal_bday_order': CASE % doys})
        order_field = 'internal_bday_order'
    else:
        qs = manager.all()
        order_field = bdoy
    if reverse:
        return qs.order_by('-%s' % order_field)
    return qs.order_by('%s' % order_field)


class BirthdayManager(models.Manager):    

    @property
    def _birthday_doy_field(self):
        return self.model._meta.birthday_field.doy_name
    
    def _doy(self, day):
        if not day:
            day = date.today()
        return day.timetuple().tm_yday
            
    def get_upcoming_birthdays(self, days=30, after=None, include_day=True, order=True, reverse=False):
        today = self._doy(after)
        limit = today + days
        q = Q(**{'%s__gt%s' % (self._birthday_doy_field, 'e' if include_day else ''): today})
        q &= Q(**{'%s__lt' % self._birthday_doy_field: limit})

        if limit > 365:
            limit = limit - 365
            today = 1
            q2 = Q(**{'%s__gte' % self._birthday_doy_field: today})
            q2 &= Q(**{'%s__lt' % self._birthday_doy_field: limit})
            q = q | q2

        if order:
            qs = _order(self, reverse, True)
            return qs.filter(q)

        return self.filter(q)
    
    def get_birthdays(self, day=None):
        return self.filter(**{self._birthday_doy_field: self._doy(day)})
    
    def order_by_birthday(self, reverse=False):
        return _order(self, reverse)
