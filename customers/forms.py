from django.forms.widgets import TextInput
from django import forms

from customers.models import OtpRecords

class LoginOtpForm(forms.ModelForm):

    class Meta:
        model = OtpRecords
        fields = ['phone']