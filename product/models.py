# standerd
import uuid
import datetime
# django
from django.db import models
from django.core.validators import MinValueValidator
#third party
from decimal import Decimal
from versatileimagefield.fields import VersatileImageField
#local
from offers.models import Offers
from main.models import BaseModel
from general.models import Location

PRODUCT_TYPE_CHOICE = (
    ('shirt', 'Shirt'),
    ('pant', 'Pant'),
    ('boxer', 'Boxer'),
    ('t_shirt', 'T-Shirt'),
)


class ProductCategory(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    
    class Meta:
        db_table = 'product_category'
        verbose_name = ('Product Category')
        verbose_name_plural = ('Product Category')
    
    def __str__(self):
        return str(self.name)
    
    def get_products(self):
        instances = Product.objects.filter(category=self,is_deleted=False)
        return instances[:4]


class Messurment(BaseModel):
    type = models.CharField(max_length=128,choices=PRODUCT_TYPE_CHOICE)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'messurment'
        verbose_name = ('Messurment')
        verbose_name_plural = ('Messurment')
        ordering = ('name',)

    def __str__(self):
        return str(self.name)
    
    
class MetaKeyword(BaseModel):
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'product_meta_keyword'
        verbose_name = ('Meta Keyword')
        verbose_name_plural = ('Meta Keyword')
    
    def __str__(self):
        return str(self.name)
    
    
class Product(BaseModel):
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    product_type = models.CharField(max_length=100,choices=PRODUCT_TYPE_CHOICE)
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    featured_image = VersatileImageField('Image', upload_to="product/product_cover", blank=True, null=True)
    meta_keywords = models.ManyToManyField(MetaKeyword)
    mrp = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    cash_on_delivery = models.BooleanField(default=False,null=True,blank=True)
    delivery_locations = models.ManyToManyField(Location,blank=True)
    
    current_rating = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))],null=True,blank=True)
    
    class Meta:
        db_table = 'product_product'
        verbose_name = ('Product')
        verbose_name_plural = ('Product')
        
    def current_price(self) : 
        current_price = self.price
        if Offers.objects.filter(is_deleted=False, to_date__gte=datetime.datetime.now(), from_date__lte=datetime.datetime.now(), product=self).exists():
            offer = Offers.objects.filter(is_deleted=False,to_date__gte=datetime.datetime.now(),from_date__lte=datetime.datetime.now(),product=self).order_by('offer_price').first()
            if offer.offer_price <= current_price:
                current_price = current_price - (current_price * offer.offer_price / 100)
        return current_price
    
    def __str__(self):
        return str(self.name)
    
    
class ProductSizeChart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand_size = models.CharField(max_length=5)
    size = models.PositiveIntegerField()
    Product_type = models.CharField(max_length=100,choices=PRODUCT_TYPE_CHOICE)
    
    waist = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    rise = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    thigh = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    inseam = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    outseam = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    bottom_hem = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    chest = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    front_length = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    across_sholder = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    sleeve_length = models.DecimalField(decimal_places=1, max_digits=15, validators=[MinValueValidator(Decimal('0.0'))],null=True,blank=True)
    
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
                
    class Meta:
        db_table = 'product_size_chart'
        verbose_name = ('Product Size Chart')
        verbose_name_plural = ('Product Size Chart')
    
    def __str__(self):
        return str(self.brand_size)
    
    
class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    stock = models.DecimalField(default=0, decimal_places=0, max_digits=15, validators=[MinValueValidator(Decimal('0'))])
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    is_default = models.BooleanField(default=False)    
           
    class Meta:
        db_table = 'product_variant'
        verbose_name = ('Product Variant')
        verbose_name_plural = ('Product Variant')
    
    def __str__(self):
        return str(self.product.name)
    
    
class ProductImage(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = VersatileImageField('Image', upload_to="product/product_carousel")
        
    class Meta:
        db_table = 'product_image'
        verbose_name = ('Product Image')
        verbose_name_plural = ('Product Image')
    
    def __str__(self):
        return str(self.product.name)
    
    
class SizeMeasurementChart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_type = models.CharField(max_length=100,choices=PRODUCT_TYPE_CHOICE)
    image = VersatileImageField('Image', upload_to="product/product_size_measurement_chart")
        
    class Meta:
        db_table = 'product_size_measurement_chart'
        verbose_name = ('Product Size Measurement Chart')
        verbose_name_plural = ('Product Size Measurement Chart')
    
    def __str__(self):
        return str(self.id)
    
