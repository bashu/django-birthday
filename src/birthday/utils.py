from datetime import date

# A real, ordinary leap year (divisible by 400, so unambiguously leap under
# the Gregorian rule) used purely as a stable reference so Feb 29 is always
# valid. Only the month/day of the input are used -- its actual year never
# affects the result, which is the whole point: the same calendar date must
# always produce the same value, regardless of which year it was recorded in.
_LEAP_YEAR = 2000


def doy(d):
    """Day-of-year (1-366) for `d`'s month/day, independent of `d`'s own
    year's leap-status."""
    return date(_LEAP_YEAR, d.month, d.day).timetuple().tm_yday
