from setuptools import setup, find_packages

version = __import__('birthday').__version__

setup(
    name = 'django-birthday',
    version = version,
    description = 'Helper field and manager for working with birthdays',
    author = 'Jonas Obrist',
    author_email = 'jonas.obrist@divio.ch',
    url = 'http://github.com/ojii/django-birthday',
    packages = find_packages(),
    zip_safe=False,
)