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