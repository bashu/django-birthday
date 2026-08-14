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