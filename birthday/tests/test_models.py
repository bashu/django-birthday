# ruff: noqa: PLR2004, SLF001
from datetime import date

from django.apps import apps
from django.core.exceptions import FieldError
from django.db import DEFAULT_DB_ALIAS
from django.db import models
from django.test import TestCase
from django.test.utils import isolate_apps

import pytest

from birthday.fields import BirthdayField
from birthday.fields import handle_pre_save
from birthday.handlers import handle_post_migrate

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
        assert doys == [1, 2, 366]
        doys = [
            obj.birthday_dayofyear_internal
            for obj in TestModel.objects.order_by_birthday(reverse=True)
        ]
        assert doys == [366, 2, 1]

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
        assert doys == [366, 1, 2]
        doys = [
            obj.birthday_dayofyear_internal
            for obj in TestModel.objects.get_upcoming_birthdays(30, dec31, reverse=True)
        ]
        assert doys == [2, 1, 366]
        doys = [
            obj.birthday_dayofyear_internal
            for obj in TestModel.objects.get_upcoming_birthdays(30, dec31, order=False)
        ]
        assert doys == [1, 2, 366]

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

    def test_handle_post_migrate(self):
        # simulate rows written before BirthdayField existed, or via
        # bulk_create()/update(), which bypass pre_save
        TestModel.objects.update(birthday_dayofyear_internal=None)

        app_config = apps.get_app_config("tests")
        handle_post_migrate(app_config, using=DEFAULT_DB_ALIAS)

        doys = sorted(
            TestModel.objects.values_list("birthday_dayofyear_internal", flat=True),
        )
        assert doys == [1, 2, 366]

    def test_issue_5(self):
        # reproduces issue #5 end-to-end: manager queries must be correct
        # again after a real backfill run
        TestModel.objects.update(birthday_dayofyear_internal=None)

        app_config = apps.get_app_config("tests")
        handle_post_migrate(app_config, using=DEFAULT_DB_ALIAS)

        jan1 = date(year=2010, month=1, day=1)
        assert TestModel.objects.get_birthdays(jan1).count() == 1
        assert TestModel.objects.get_upcoming_birthdays(30, jan1).count() == 2

    def test_issue_8(self):
        # 2000 is leap, 2001 is not -- same calendar day must produce the
        # same cached day-of-year regardless.
        #
        # born in a leap year, matched on the same month/day in a non-leap year
        leap_born = TestModel.objects.create(birthday=date(2000, 3, 15))
        assert leap_born in TestModel.objects.get_birthdays(date(2023, 3, 15))

        # born in a non-leap year, matched on the same month/day in a leap year
        nonleap_born = TestModel.objects.create(birthday=date(2001, 3, 15))
        assert nonleap_born in TestModel.objects.get_birthdays(date(2024, 3, 15))

        leap_born.refresh_from_db()
        nonleap_born.refresh_from_db()

        assert (
            leap_born.birthday_dayofyear_internal
            == nonleap_born.birthday_dayofyear_internal
        )

    @isolate_apps("birthday.tests")
    def test_exception(self):
        class BrokenModel(models.Model):
            birthday = BirthdayField()

            def __str__(self):
                return "broken"

        with pytest.raises(FieldError):
            BirthdayField().contribute_to_class(BrokenModel, "another_birthday")
