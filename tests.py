from django.core.management import call_command
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'testapp._settings'

if __name__ == '__main__':
    call_command('test', 'testapp')
