from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput
from django import forms
from . models import *

class OffersForm(forms.ModelForm):

    class Meta:
        model = Offers
        fields = ['product','from_date','to_date','offer_price']

        widgets = {
            'product': Select(attrs={'class': 'form-control selectpicker'}),
            'from_date': DateInput(attrs={'class': 'required form-control date-picker','id' : 'mdate','autocomplete' : 'off' }),
            'to_date': DateInput(attrs={'class': 'required form-control date-picker','id' : 'mdate2','autocomplete' : 'off' }),
            'offer_price': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Offer Price'}),
            
        }