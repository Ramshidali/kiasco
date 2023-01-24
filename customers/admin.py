from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(OtpRecords)
admin.site.register(OtpEmailRecords)
admin.site.register(Customer)
admin.site.register(CustomerAddress)
admin.site.register(WhishlistItem)
admin.site.register(CartItem)
admin.site.register(CustomerReview)