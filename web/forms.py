#django
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput
from django import forms
#local
from customers.models import CustomerAddress, CustomerReview
from orders.models import Order, OrderItem
from payments.models import Payment
from product.models import Product
from . models import *

class BannersForm(forms.ModelForm):

    class Meta:
        model = Banner
        fields = ['image','product']

        widgets = {
            'product': Select(attrs={'class': 'select2 form-control mb-3 custom-select','placeholder' : 'Select Product'}),
            'image': FileInput(attrs={'class': 'form-control dropify'}),
        }

    def clean_image(self):

        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png")):
            raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file

class AddressForm(forms.ModelForm):

    class Meta:
        model = CustomerAddress
        fields = ['name','phone','pincode','locality','address','city','state']

        widgets = {
            'location' : TextInput(attrs={'name':'name','placeholder':'Location'}),
            'name' : TextInput(attrs={'name':'name','placeholder':'Name'}),
            'phone' : TextInput(attrs={'name':'mobile-number','placeholder':'Phone'}),
            'pincode' : TextInput(attrs={'name':'pincode','placeholder':'Pincode','class':'address-pincode'}),
            'locality' : TextInput(attrs={'name':'locality','placeholder':'Locality'}),
            'address' : Textarea(attrs={'name':'address','placeholder':'Address'}),
            'city' : TextInput(attrs={'name':'city','placeholder':'City'}),
            'state' : TextInput(attrs={'name':'state','placeholder':'State'}),
        }


class RatingForm(forms.ModelForm):
    rating = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = CustomerReview
        fields = ['rating','review']


class CancelReasonForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['cancel_reason']

        widgets = {
            'cancel_reason' : Textarea(attrs={'placeholder':'Enter Reason'}),
        }

class AboutDescriptionForm(forms.ModelForm):

    class Meta:
        model = AboutDescription
        fields = ['description']

        widgets = {
            'description' :  Textarea(attrs={'class': 'form-control'}),
        }
class AboutGalleryForm(forms.ModelForm):

    class Meta:
        model = AboutGallery
        fields = ['image']

        widgets = {
            'description' :  Textarea(attrs={'class': 'form-control'}),
        }

class AboutCustomerReviewForm(forms.ModelForm):

    class Meta:
        model = AboutCustomerReview
        fields = ['rating','name','designation','description','image']

        widgets = {
            'description' :  Textarea(attrs={'class': 'form-control'}),
            'name' :  TextInput(attrs={'class': 'form-control'}),
            'designation' :  TextInput(attrs={'class': 'form-control'}),
            'rating' :  TextInput(attrs={'class': 'form-control'}),
        }