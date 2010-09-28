from birthday.fields import BirthdayField
from birthday.managers import BirthdayManager
from django.db import models

class TestModel(models.Model):
    birthday = BirthdayField()
    
    objects = BirthdayManager()
    
    class Meta:
        ordering = ['id']
        
        
class TestModel2(models.Model):
    birthday = BirthdayField(null=True)
    
    objects = BirthdayManager()