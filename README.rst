django-birthday
===============

django-birthday is a helper library to work with birthdays in models.

Authored by `Jonas Obrist <https://github.com/ojii>`_,  and some great
`contributors <https://github.com/bashu/django-birthday/contributors>`_.

.. image:: https://img.shields.io/pypi/v/django-birthday.svg
    :target: https://pypi.python.org/pypi/django-birthday/

.. image:: https://img.shields.io/pypi/dm/django-birthday.svg
    :target: https://pypi.python.org/pypi/django-birthday/

.. image:: https://img.shields.io/github/license/bashu/django-birthday.svg
    :target: https://pypi.python.org/pypi/django-birthday/

.. image:: https://img.shields.io/travis/bashu/django-birthday.svg
    :target: https://travis-ci.org/bashu/django-birthday/

Installation
------------

.. code-block:: bash

    pip install django-birthday

Usage
-----

django-birthday provides a ``birthday.fields.BirthdayField`` model
field type which is a subclass of ``django.db.models.DateField`` and
thus has the same characteristics as that. It also internally adds a
second field to your model holding the day of the year for that
birthday, this is used for the extra functionality exposed by
``birthday.managers.BirthdayManager`` which you should use as the
manager on your model.

A model could look like this:

.. code-block:: python

    from django.db import models

    import birthday


    class UserProfile(models.Model):
        user = models.ForeignKey('auth.User')
        birthday = birthday.fields.BirthdayField()

        objects = birthday.managers.BirthdayManager()

Get all user profiles within the next 30 days:

.. code-block:: python

    UserProfile.objects.get_upcoming_birthdays()

Get all user profiles which have their birthday today:

.. code-block:: python

    UserProfile.objects.get_birthdays()

Or order the user profiles according to their birthday:

.. code-block:: python

    UserProfile.objects.order_by_birthday()

For more details, see the documentation_ at Read The Docs.

License
-------

``django-birthday`` is released under the BSD license.

.. _documentation: https://django-birthday.readthedocs.io/
