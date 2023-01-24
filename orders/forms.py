from django import forms
from django.forms.widgets import TextInput, Textarea, HiddenInput, Select, FileInput,DateInput
from django.utils.translation import ugettext_lazy as _
from orders.models import *


class OrderStatusForm(forms.Form):
    ORDER_CHOICES = (
            ("pending", 'Pending'),
            ("shipped", 'Shipped'),
            ("delivered", 'Delivered'),
            ("cancelled", 'Cancelled'),
        )
    order_status = forms.CharField(widget=forms.Select(choices=ORDER_CHOICES, attrs={'class':'form-control selectpicker'}))
        
        
class OrderTrackingForm(forms.ModelForm):
    
    class Meta:
        model = OrderTracking
        exclude = ['creator','updater','auto_id','is_deleted','order']
        widgets = {
            'expected_date': TextInput(attrs={'class': 'required form-control ','autocomplete' : 'off', 'type': 'date'}),
            'delivery_partner': TextInput(attrs={'class': 'required form-control','placeholder' : 'Delivery partner'}),
            'tracking_id': TextInput(attrs={'class': 'required form-control','placeholder' : 'Tracking ID'}),
        }
        error_messages = {
            
        }
        