Changes
-------

0.1.4 (WIP)
~~~~~~~~~~~~~~~~~~

* Added an automatic ``post_migrate`` handler that backfills the cached
  day-of-year column for pre-existing rows and rows written via
  ``bulk_create()``/``update()`` whose value was never computed, so
  ``BirthdayManager`` queries are correct without manual intervention (#5).
* Fixed the cached day-of-year column being computed from each date's own
  actual year, which made it inconsistent for the same calendar day across
  leap and non-leap years and caused ``BirthdayManager`` to silently miss
  or misorder matching birthdays (#8). Day-of-year is now always computed
  relative to a fixed reference year, independent of leap status.
