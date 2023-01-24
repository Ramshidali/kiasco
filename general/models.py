#statnderd
from pyexpat import model
from secrets import choice
import uuid
#django
from django.db import models
from django.core.validators import MinValueValidator
#third party
from decimal import Decimal
#local
from main.models import BaseModel
from . models import *


AREA_CHOICES = (
    ('kerala_state', 'Kerala State'),
    ('other_state', 'Other State'),
)

# Create your models here.    
class Location(BaseModel):
    area = models.CharField(max_length=20,choices=AREA_CHOICES,null=True, blank=True)
    min_day_of_delivery = models.PositiveIntegerField()
    delivery_charge = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        db_table = 'general_location'
        verbose_name = ('Location')
        verbose_name_plural = ('Location')

    def __str__(self):
        return f'{self.area}'

class Contacts(models.Model):
    android_app_link = models.URLField(null=True, blank=True)
    ios_app_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    pinterest_link = models.URLField(null=True, blank=True)
    behance_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    whatsapp_link = models.URLField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    whatsapp_number = models.CharField(max_length=64,null=True, blank=True)

    class Meta:
        db_table = 'web_contact'
        verbose_name = 'contacts'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return str(self.id)