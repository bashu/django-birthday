=====
Usage
=====

django-birthday provides a :class:`birthday.fields.BirthdayField` model field
type which is a subclass of :class:`django.db.models.DateField` and thus has the
same characteristics as that. It also internally adds a second field to your
model holding the day of the year for that birthday, this is used for the extra
functionality exposed by :class:`birthday.managers.BirthdayManager` which you
should use as the manager on your model.


A model could look like this::

    import birthday
    from django.db import models
    
    class UserProfile(models.Model):
        user = models.ForeignKey('auth.User')
        birthday = birthday.fields.BirthdayField()
        
        objects = birthday.managers.BirthdayManager()
        
        
Get all user profiles within the next 30 days::

    UserProfile.objects.get_upcoming_birthdays()
    
Get all user profiles which have their birthday today::

    UserProfile.objects.get_birthdays()
    
Or order the user profiles according to their birthday::

    UserProfile.objects.order_by_birthday()


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