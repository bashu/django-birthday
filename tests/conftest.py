from datetime import date

import pytest

from .models import TestModel


@pytest.fixture
def birthdays(db: None) -> list[TestModel]:
    """Rows born on Jan 1, Jan 2 and Dec 31 of different years."""
    return [
        TestModel.objects.create(birthday=date.fromisoformat(birthday))
        for birthday in ["2001-01-01", "2000-01-02", "2002-12-31"]
    ]
