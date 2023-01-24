#standard
import uuid
#django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal
#local
from main.models import BaseModel
from general.models import Location
from product.models import Product, ProductVariant


# Create your models here.

GENDER_CHOICE = (
    ("10", "Male"),
    ("20", "Female"),
)

class OtpRecords(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=10)
    otp = models.CharField(max_length=4)
    attempts = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = ('Otp Phone Record')
        verbose_name_plural = ('Otp Phone Records')

    def __str__(self):
        return f'{self.phone} - {self.otp}'
    

class OtpEmailRecords(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    otp = models.CharField(max_length=4)
    attempts = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = ('Otp Email Record')
        verbose_name_plural = ('Otp Email Records')

    def __str__(self):
        return f'{self.email} - {self.otp}'

    
class Customer(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    password = models.CharField(max_length=256)
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    gender = models.CharField(choices=GENDER_CHOICE,max_length=2)
        
    class Meta:
        db_table = 'customers_customer'
        verbose_name = ('Customer')
        verbose_name_plural = ('Customer')
    
    def __str__(self):
        return str(self.name)
    
    
class CustomerAddress(BaseModel):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    pincode = models.IntegerField()
    locality = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
               
    class Meta:
        db_table = 'customers_customer_address'
        verbose_name = ('Customer Address')
        verbose_name_plural = ('Customer Address')
    
    def __str__(self):
        return str(self.name)
    
class WhishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'customers_whishlist'
        verbose_name = ('Whishlist')
        verbose_name_plural = ('Whishlist')
    
    def __str__(self):
        return f'{self.customer.name} - {self.product.name}'
    
    
class CartItem(BaseModel):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product_varient = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    unit_price = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        db_table = 'customers_cart_item'
        verbose_name = ('Cart Item')
        verbose_name_plural = ('Cart Item')
    
    def __str__(self):
        return f'{self.customer.name} - {self.product_varient.product.name}'
    
    
class CustomerReview(BaseModel):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField(blank=True,null=True)
        
    class Meta:
        db_table = 'customer_review'
        verbose_name = ('Customer Review')
        verbose_name_plural = ('Customer Review')
    
    def __str__(self):
        return f'{self.customer.name} - {self.product.name} - {self.rating}'