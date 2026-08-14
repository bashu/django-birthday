Changes
-------

0.1.4 (WIP)
~~~~~~~~~~~~~~~~~~

* Added an automatic ``post_migrate`` handler that backfills the cached
  day-of-year column for pre-existing rows and rows written via
  ``bulk_create()``/``update()`` whose value was never computed, so
  ``BirthdayManager`` queries are correct without manual intervention (#5).
