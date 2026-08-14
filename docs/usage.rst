=====
Usage
=====

django-birthday provides a :class:`birthday.fields.BirthdayField` model field
type which is a subclass of :class:`django.db.models.DateField` and thus has the
same characteristics as that. It also internally adds a second field to your
model holding the day of the year for that birthday, this is used for the extra
functionality exposed by :class:`birthday.managers.BirthdayManager` which you
should use as the manager on your model.


A model could look like this:

.. code-block:: python

    from django.db import models
    from django.conf import settings
    
    from birthday import BirthdayField, BirthdayManager


    class UserProfile(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL)
        birthday = BirthdayField()
        
        objects = BirthdayManager()
        
        
Get all user profiles within the next 30 days:

.. code-block:: python

    UserProfile.objects.get_upcoming_birthdays()
    
Get all user profiles which have their birthday today:

.. code-block:: python

    UserProfile.objects.get_birthdays()
    
Or order the user profiles according to their birthday:

.. code-block:: python

    UserProfile.objects.order_by_birthday()


Automatic backfill on migrate
------------------------------

The cached day-of-year column is normally kept in sync by a ``pre_save``
signal receiver. Any row written *before* your model started using
:class:`birthday.fields.BirthdayField` -- or written via
:meth:`~django.db.models.query.QuerySet.bulk_create` or
:meth:`~django.db.models.query.QuerySet.update`, both of which bypass
``pre_save`` -- would otherwise end up with an empty cache, and
:class:`birthday.managers.BirthdayManager` would silently return incomplete
results for those rows.

django-birthday registers a ``post_migrate`` handler that runs automatically
every time you run ``manage.py migrate``. For every model in every installed
app that uses a :class:`birthday.fields.BirthdayField`, it finds rows whose
cached value has never been computed and backfills it, in efficient batches,
without loading whole tables into memory and without re-triggering
``pre_save`` for every row.

This is fully automatic -- nothing to configure, and nothing to run by hand.
If you add ``BirthdayField`` to an existing model with existing data, running
``manage.py migrate`` afterwards (Django always emits the ``post_migrate``
signal, even when there's nothing new to apply) will bring the cache up to
date.


Method References
-----------------

.. method:: birthday.managers.BirthdayManager.get_upcoming_birthdays

    Returns a queryset containing objects that have an upcoming birthday.

    :param days: *Optional*. Amount of days that still count as 'upcoming',
                 defaults to 30.
    :param after: *Optional*. Start day to use, defaults to 'today'.
    :param include_day: *Optional*. Include the 'after' day for lookups.
    :param order: *Optional*. Whether the queryset should be ordered by birthday,
                  defaults to True.
    :param reverse: *Optional*. Only applies when `order` is True. Apply
                    reverse ordering.
    :rtype: Instance of :class:`django.db.models.query.QuerySet`.
    
    
.. method:: birthday.managers.BirthdayManager.get_birthdays
    
    Returns a queryset containing objects which have the birthday on a specific
    day.
    
    :param day: *Optional*. What day to get the birthdays of. Defaults to
        'today'.
    :rtype: Instance of :class:`django.db.models.query.QuerySet`.
    
   
.. method:: birthday.managers.BirthdayManager.order_by_birthday

    Returns a queryset ordered by birthday (not age!).
    
    :param reverse: *Optional*. Defaults to `False`. Whether or not to reverse
        the results.
    :rtype: Instance of :class:`django.db.models.query.QuerySet`.
