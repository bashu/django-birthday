# ruff: noqa: PLR2004, SLF001
from datetime import date

from django.core.exceptions import FieldError
from django.db import models
from django.test import TestCase

import pytest

from birthday.fields import BirthdayField
from birthday.fields import handle_pre_save

from .models import TestModel


class BirthdayTest(TestCase):
    def setUp(self):
        for birthday in ["2001-01-01", "2000-01-02", "2002-12-31"]:
            TestModel.objects.create(birthday=date.fromisoformat(birthday))

    def test_default(self):
        assert len(TestModel._meta.fields) == 3
        assert hasattr(TestModel._meta, "birthday_field")
        assert TestModel.objects.all().count() == 3

    def test_ordering(self):
        pks1 = [obj.pk for obj in TestModel.objects.order_by("birthday")]
        pks2 = [obj.pk for obj in TestModel.objects.order_by_birthday()]
        assert pks1 != pks2

        doys = [
            obj.birthday_dayofyear_internal
            for obj in TestModel.objects.order_by_birthday()
        ]
        assert doys == [1, 2, 365]
        doys = [
            obj.birthday_dayofyear_internal
            for obj in TestModel.objects.order_by_birthday(reverse=True)
        ]
        assert doys == [365, 2, 1]

        years = [obj.birthday.year for obj in TestModel.objects.order_by("birthday")]
        assert years == [2000, 2001, 2002]

    def test_manager(self):
        jan1 = date(year=2010, month=1, day=1)
        assert TestModel.objects.get_birthdays(jan1).count() == 1
        assert TestModel.objects.get_upcoming_birthdays(30, jan1).count() == 2
        upcoming = TestModel.objects.get_upcoming_birthdays(30, jan1, include_day=False)
        assert upcoming.count() == 1

        dec31 = date(year=2010, month=12, day=31)
        assert TestModel.objects.get_birthdays(dec31).count() == 1
        assert TestModel.objects.get_upcoming_birthdays(30, dec31).count() == 3

        doys = [
            obj.birthday_dayofyear_internal
            for obj in TestModel.objects.get_upcoming_birthdays(30, dec31)
        ]
        assert doys == [365, 1, 2]
        doys = [
            obj.birthday_dayofyear_internal
            for obj in TestModel.objects.get_upcoming_birthdays(30, dec31, reverse=True)
        ]
        assert doys == [2, 1, 365]
        doys = [
            obj.birthday_dayofyear_internal
            for obj in TestModel.objects.get_upcoming_birthdays(30, dec31, order=False)
        ]
        assert doys == [1, 2, 365]

        upcoming = TestModel.objects.get_upcoming_birthdays(
            30,
            dec31,
            include_day=False,
        )
        assert upcoming.count() == 2
        assert TestModel.objects.get_birthdays().count() in [0, 1]

    def test_handle_pre_save(self):
        instance = TestModel(birthday=None)
        instance.birthday_dayofyear_internal = 42
        handle_pre_save(instance)
        assert instance.birthday_dayofyear_internal == 42

    def test_exception(self):
        class BrokenModel(models.Model):
            birthday = BirthdayField()

            def __str__(self):
                return "broken"

        with pytest.raises(FieldError):
            BirthdayField().contribute_to_class(BrokenModel, "another_birthday")
