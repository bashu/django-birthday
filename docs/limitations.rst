===========
Limitations
===========

There are a couple of limitations for django-birthday:

* You can only have **one** :class:`birthday.fields.BirthdayField` field on a
  single model.
* You cannot chain the custom methods provided by the manager.
* Ordering by a :class:`birthday.fields.BirthdayField` while not using
  :meth:`birthday.managers.BirthdayManager.order_by_birthday` will order by
  **age**, not when their birthday is in a year.
* The automatic ``post_migrate`` backfill (see :doc:`usage`) only fills in
  rows whose cached day-of-year is still empty; it does not detect or repair
  a cache that has gone *stale* after being set once (for example, if you
  change a birthday via ``update()`` or raw SQL, which also bypasses
  ``pre_save``). Re-save the affected instances in that case.
* A birthday recorded as **February 29** has no exact calendar match via
  :meth:`birthday.managers.BirthdayManager.get_birthdays` during non-leap
  years, since there is no real February 29 that year to match against.
  Whether such birthdays should be treated as February 28 or March 1 in
  off-years is a policy decision left to the application, not something
  django-birthday decides on your behalf.