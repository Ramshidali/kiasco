import profile
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator,MaxValueValidator
from versatileimagefield.fields import VersatileImageField
from main.models import BaseModel
from product.models import Product

# Create your models here.

class Testimonials(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    rating = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    profile_picture = VersatileImageField('Image', upload_to="web/testimonials", blank=True, null=True)

    class Meta:
        db_table = 'web_testimonials'
        verbose_name = ('Testimonials')
        verbose_name_plural = ('Testimonials')

    def __str__(self):
        return str(self.name)

class Gallery(BaseModel):
    name = models.CharField(max_length=200)
    profile_picture = VersatileImageField('Image', upload_to="web/gallery", blank=True, null=True)

    class Meta:
        db_table = 'web_gallery'
        verbose_name = ('Gallery')
        verbose_name_plural = ('Gallery')

class Banner(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = VersatileImageField('Image', upload_to="web/banner", blank=True, null=True)

    class Meta:
        db_table = 'web_banner'
        verbose_name = ('Banner')
        verbose_name_plural = ('Banner')

class AboutDescription(BaseModel):
    description = models.TextField()

    class Meta:
        db_table = 'web_about_description'
        verbose_name = ('About Description')
        verbose_name_plural = ('About Description')

    def __str__(self):
        return str(self.description)

class AboutGallery(BaseModel):
    image = VersatileImageField('Image', upload_to="web/about_gallery",help_text='230 x 230')

    class Meta:
        db_table = 'web_about_gallery'
        verbose_name = ('About Gallery')
        verbose_name_plural = ('About Gallery')

class AboutCustomerReview(BaseModel):
    rating = models.DecimalField(default=0, decimal_places=0, max_digits=1, validators=[MinValueValidator(Decimal('0')),MaxValueValidator(Decimal('5'))])
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    description = models.TextField()
    image = VersatileImageField('Image', upload_to="web/about_customer_review")
    class Meta:
        db_table = 'web_customer_review'
        verbose_name = ('Customer Review')
        verbose_name_plural = ('Customer Review')

    def __str__(self):
        return str(self.name)

