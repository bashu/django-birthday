# -*- coding: utf-8 -*-

from datetime import date, datetime

from django.core.exceptions import FieldError
from django.db import models
from django.test import TestCase

from birthday.fields import BirthdayField
from birthday.managers import BirthdayManager

from .models import TestModel


class BirthdayTest(TestCase):
    def setUp(self):
        for birthday in ["2001-01-01", "2000-01-02", "2002-12-31"]:
            TestModel.objects.create(birthday=datetime.strptime(birthday, "%Y-%m-%d").date())

    def test_default(self):
        self.assertEqual(len(TestModel._meta.fields), 3)
        self.assertTrue(hasattr(TestModel._meta, "birthday_field"))
        self.assertEqual(TestModel.objects.all().count(), 3)

    def test_ordering(self):
        pks1 = [obj.pk for obj in TestModel.objects.order_by("birthday")]
        pks2 = [obj.pk for obj in TestModel.objects.order_by_birthday()]
        self.assertNotEqual(pks1, pks2)

        doys = [getattr(obj, "birthday_dayofyear_internal") for obj in TestModel.objects.order_by_birthday()]
        self.assertEqual(doys, [1, 2, 365])
        doys = [getattr(obj, "birthday_dayofyear_internal") for obj in TestModel.objects.order_by_birthday(True)]
        self.assertEqual(doys, [365, 2, 1])

        years = [obj.birthday.year for obj in TestModel.objects.order_by("birthday")]
        self.assertEqual(years, [2000, 2001, 2002])

    def test_manager(self):
        jan1 = date(year=2010, month=1, day=1)
        self.assertEqual(TestModel.objects.get_birthdays(jan1).count(), 1)
        self.assertEqual(TestModel.objects.get_upcoming_birthdays(30, jan1).count(), 2)
        self.assertEqual(TestModel.objects.get_upcoming_birthdays(30, jan1, False).count(), 1)

        dec31 = date(year=2010, month=12, day=31)
        self.assertEqual(TestModel.objects.get_birthdays(dec31).count(), 1)
        self.assertEqual(TestModel.objects.get_upcoming_birthdays(30, dec31).count(), 3)

        doys = [
            getattr(obj, "birthday_dayofyear_internal") for obj in TestModel.objects.get_upcoming_birthdays(30, dec31)
        ]
        self.assertEqual(doys, [365, 1, 2])
        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in TestModel.objects.get_upcoming_birthdays(30, dec31, reverse=True)
        ]
        self.assertEqual(doys, [2, 1, 365])
        doys = [
            getattr(obj, "birthday_dayofyear_internal")
            for obj in TestModel.objects.get_upcoming_birthdays(30, dec31, order=False)
        ]
        self.assertEqual(doys, [1, 2, 365])

        self.assertEqual(TestModel.objects.get_upcoming_birthdays(30, dec31, False).count(), 2)
        self.assertTrue(TestModel.objects.get_birthdays().count() in [0, 1])

    def test_exception(self):
        class BrokenModel(models.Model):
            birthday = BirthdayField()

        self.assertRaises(FieldError, BirthdayField().contribute_to_class, BrokenModel, "another_birthday")
