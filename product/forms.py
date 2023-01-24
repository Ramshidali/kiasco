from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput
from django import forms
from . models import *
from dal import autocomplete

class MetaKeywordsForm(forms.ModelForm):

    class Meta:
        model = MetaKeyword
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Title'}),
        }

class ProductForm(forms.ModelForm):
    
    cash_on_delivery = forms.BooleanField(required=False)
    
    class Meta:
        model = Product
        fields = ['name','category','product_type','short_description','description','featured_image','meta_keywords','mrp','price','current_rating','cash_on_delivery']
            
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Name'}),
            'category': Select(attrs={'class': 'select2 form-control mb-3 custom-select','placeholder' : 'Enter Category'}),
            'product_type': Select(attrs={'class': 'select2 form-control mb-3 custom-select','placeholder' : 'Select Product Type'}),
            'short_description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter short_description'}),
            'description': Textarea(attrs={'class': 'required form-control text-area','placeholder' : 'Enter Description'}),
            'featured_image': FileInput(attrs={'class': 'form-control dropify'}), 
            'meta_keywords': autocomplete.ModelSelect2Multiple(url='product:meta_keywords_autocomplete',
                attrs={'class': 'select2 form-control meta_keywords','data-placeholder': 'Meta Keywords','data-minimum-input-length': 0}),
            'mrp': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter mrp'}),
            'price': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter price'}),
            'current_rating': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter current rating'}),
        }
        
    def clean_image(self):
        
        image_file = self.cleaned_data.get('featured_image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
            raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file

class ProductImageForm(forms.ModelForm):
    
    class Meta:
        model = ProductImage
        fields = ['image']
        
        widgets ={
            'image': FileInput(attrs={'class': 'form-control dropify'}), 
        }
        
    def clean_image(self):
        
        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
            raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file
    
class ProductVariantForm(forms.ModelForm):
    
    class Meta:
        model = ProductVariant
        fields = ['size','stock','is_default']

        widgets = {
            'size': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Brand Size'}),
            'stock': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter stock'}),
        }
        
class SizeChartForm(forms.ModelForm):
    
    class Meta:
        model = ProductSizeChart
        exclude = ['id','Product_type','is_deleted']

        widgets = {
            'brand_size': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Brand Size'}),
            'size': TextInput(attrs={'class': 'required form-control h-20','placeholder' : 'Enter Size'}),
            
            'chest': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter chest'}),
            'front_length': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter front length'}),
            'across_sholder': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter across sholder'}),
            'waist': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter waist'}),
            'sleeve_length': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter sleave length'}),
            'outseam': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter outseam'}),
            'inseam': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter inseam'}),
            'bottom_hem': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter bottom hem'}),
            'rise': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter waist'}),
            'thigh': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter waist'}),
        }
        
class SizeChartImageForm(forms.ModelForm):
    
    class Meta:
        model = SizeMeasurementChart
        fields = ['image']
        
        widgets ={
            'image': FileInput(attrs={'class': 'form-control dropify'}), 
        }
        
    def clean_image(self):
        
        image_file = self.cleaned_data.get('image')
        if not (image_file.name.endswith(".jpg") or image_file.name.endswith(".png") or image_file.name.endswith(".jpeg")):
            raise forms.ValidationError("Only .jpg or .png files are accepted")
        return image_file


    
class ProductCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ProductCategory
        exclude = ['creator','updater','auto_id','is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ','autocomplete' : 'off', 'placeholder' : 'Name'}),
            'description': TextInput(attrs={'class': 'required form-control','placeholder' : 'Description'}),
        }
        error_messages = {
            'name': {
                'required': ("Name field is required."),
            },  
        }
        
        
# class ProductTypeForm(forms.ModelForm):
    
#     class Meta:
#         model = ProductType
#         exclude = ['creator', 'updater','deleted_reason', 'auto_id', 'is_deleted']
#         widgets = {
#             'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Name'}),
#             'category': autocomplete.ModelSelect2(url='product:category_autocomplete', attrs={'data-placeholder': 'Category', 'class': 'required', 'data-minimum-input-length': 0}),
#         }

#         error_messages = {
#             'name': {
#                 'required': ("Name field is required."),
#             },
#             'category': {
#                 'required': ("Category field is required."),
#             },
#         }