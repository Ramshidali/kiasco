from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from main.models import BaseModel


class Offers(BaseModel):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    offer_price = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        db_table = 'product_offers'
        verbose_name = ('Offers')
        verbose_name_plural = ('Offers')
    
    def __str__(self):
        return str(self.product.name)