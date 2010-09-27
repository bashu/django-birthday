from _settings_patcher import *
from birthday.fields import BirthdayField
from datetime import date
from django.core.exceptions import FieldError
from django.db import models
from django.test import TestCase
from testapp.models import TestModel, TestModel2
import os

thisdir = os.path.abspath(os.path.dirname(__file__))
fixture = os.path.join(thisdir, 'fixtures', 'testdata.json')

class BirthdayTests(TestCase):
    fixtures = [fixture]
    def test_01_basic(self):
        # auto-id-field + birthday-field + internal-birthday-field
        self.assertEqual(len(TestModel._meta.fields), 3)
        self.assertTrue(hasattr(TestModel._meta, 'birthday_field'))
        self.assertEqual(TestModel.objects.all().count(), 3)
        
    def test_02_ordering(self):
        field = TestModel._meta.birthday_field
        pks1 = [obj.pk  for obj in TestModel.objects.order_by('birthday')]
        pks2 = [obj.pk  for obj in TestModel.objects.order_by_birthday()]
        self.assertNotEqual(pks1, pks2)
        doys = [getattr(obj, field.doy_name)  for obj in TestModel.objects.order_by_birthday()]
        self.assertEqual(doys, [1,2,365])
        doys = [getattr(obj, field.doy_name)  for obj in TestModel.objects.order_by_birthday(True)]
        self.assertEqual(doys, [365, 2, 1])
        years = [obj.birthday.year  for obj in TestModel.objects.order_by('birthday')]
        self.assertEqual(years, [2000, 2001, 2002])
        
        
    def test_03_manager(self):
        jan1 = date(year=2010, month=1, day=1)
        self.assertEqual(TestModel.objects.get_birthdays(jan1).count(), 1)
        self.assertEqual(TestModel.objects.get_upcoming_birthdays(30, jan1).count(), 2)
        self.assertEqual(TestModel.objects.get_upcoming_birthdays(30, jan1, False).count(), 1)
        dec31 = date(year=2010, month=12, day=31)
        self.assertEqual(TestModel.objects.get_birthdays(dec31).count(), 1)
        self.assertEqual(TestModel.objects.get_upcoming_birthdays(30, dec31).count(), 3)
        self.assertEqual(TestModel.objects.get_upcoming_birthdays(30, dec31, False).count(), 2)
        self.assertTrue(TestModel.objects.get_birthdays().count() in [0,1])
        
    def test_04_exceptions(self):
        class FailModel(models.Model):
            bd1 = BirthdayField()
        bdf2 = BirthdayField()
        self.assertRaises(
            FieldError,
            bdf2.contribute_to_class,
            FailModel,
            'bdf2'
        )