#django
from django.db import models
from django.core.validators import MinValueValidator
#local
from customers.models import Customer, CustomerAddress
from main.models import BaseModel
from payments.models import Payment
from product.models import ProductVariant
#thirdparty
from decimal import Decimal


# Create your models here.
PAYMENT_METHOD_CHOICE = (
    ('cash_on_delivery', 'Cash On Delivery'),
    ('online_payment', 'Online Payment'),
)
ORDER_STATUS_CHOICE = (
    ('pending', 'Pending'),
    ('return', 'Return'),
    ('ordered', 'Ordered'),
    ('shipped', 'Shipped'),
    ('out_of_delivered', 'Out of Delivered'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

PAYMENT_STATUS_CHOICE = (
    ('pending','Pending'),
    ('received','Received'),
    ('failed','Failed'),
)


class TempAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerAddress,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'temp_address'
        verbose_name = ('Temp Address')
        verbose_name_plural = ('Temp Address')
         

class Order(BaseModel):
    order_id = models.CharField(max_length=50)
    time = models.DateTimeField()
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    billing_name = models.CharField(max_length=200)
    billing_phone = models.CharField(max_length=10)
    billing_pincode = models.IntegerField()
    billing_locality = models.CharField(max_length=200)
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=200)
    billing_state = models.CharField(max_length=200)
    total_amount = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    payment_method = models.CharField(max_length=100,choices=PAYMENT_METHOD_CHOICE)
    payment_status = models.CharField(max_length=100,choices=PAYMENT_STATUS_CHOICE,default='failed')
    
    
    class Meta:
        db_table = 'orders_order'
        verbose_name = ('Order')
        verbose_name_plural = ('Order')
    
    def __str__(self):
        return str(self.order_id)
    
class OrderItem(BaseModel):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_varient = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    qty = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    subtotal = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    order_status = models.CharField(default="pending", max_length=100,choices=ORDER_STATUS_CHOICE)
    cancel_reason = models.TextField(null=True,blank=True)
    
    class Meta:
        db_table = 'orders_order_item'
        verbose_name = ('Order Item')
        verbose_name_plural = ('Order Item')
    
    def __str__(self):
        return str(self.order)
    
    
class OrderTracking(BaseModel):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    delivery_partner = models.CharField(max_length=50)
    tracking_id = models.CharField(max_length=50)
    expected_date = models.DateField()   
    
    class Meta:
        db_table = 'orders_order_tracking'
        verbose_name = ('Order Tracking')
        verbose_name_plural = ('Order Tracking')
    
    def __str__(self):
        return str(self.order)