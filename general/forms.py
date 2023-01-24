from django.forms.widgets import TextInput, Textarea, Select, DateInput, CheckboxInput, FileInput, EmailInput
from django import forms

from general.models import Contacts, Location


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ['area','delivery_charge', 'min_day_of_delivery']

        widgets = {
            'area': Select(attrs={'class': 'select2 form-control mb-3 custom-select','placeholder' : 'Select Area'}),
            'delivery_charge': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Delivery Charge'}),
            'min_day_of_delivery': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter min day of delivey'}),
        }


class ContactsForm(forms.ModelForm):

    class Meta:
        model = Contacts
        fields = ('whatsapp_link',
                  'facebook_link',
                  'instagram_link',
                  'twitter_link',)
        widgets = {
            'whatsapp_number': TextInput(attrs={'class': 'form-control'}),
            'facebook_link': TextInput(attrs={'class': ' form-control'}),
            'instagram_link': TextInput(attrs={'class': ' form-control'}),
            'twitter_link': TextInput(attrs={'class': ' form-control'}),
            'android_app_link': TextInput(attrs={'class': ' form-control'}),
            'ios_app_link': TextInput(attrs={'class': ' form-control'}),
            'pinterest_link': TextInput(attrs={'class': ' form-control'}),
            'behance_link': TextInput(attrs={'class': ' form-control'}),
            'whatsapp_link': TextInput(attrs={'class': ' form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }


class FileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control file-upload-info file-upload-default', 'id' : 'input-file-now'}))