from birthday.fields import BirthdayField
from datetime import date
from django.db.models.manager import Manager
from django.db.models.query_utils import Q

class BirthdayManager(Manager):    
    @property
    def _birthday_doy_field(self):
        return self.model._meta.birthday_field.doy_name
    
    def _doy(self, day):
        if not day:
            day = date.today()
        return day.timetuple().tm_yday
            
    def get_upcoming_birthdays(self, days=30, after=None, include_day=True):
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
        return self.filter(q)
    
    def get_birthdays(self, day=None):
        today = self._doy(day)
        return self.filter(**{self._birthday_doy_field: today})
    
    def order_by_birthday(self, reverse=False):
        if reverse:
            return self.order_by('-%s' % self._birthday_doy_field)
        return self.order_by(self._birthday_doy_field)