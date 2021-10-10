# Generated by Django 3.2.7 on 2021-10-09 06:41

import birthday.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211009_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='birthday_dayofyear_internal',
            field=models.PositiveSmallIntegerField(default=None, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=birthday.fields.BirthdayField(blank=True, null=True),
        ),
    ]
