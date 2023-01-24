from django.contrib import admin
from . models import *

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','order_id','customer']
admin.site.register(Order,OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'qty', 'subtotal','order_status', 'cancel_reason',]
admin.site.register(OrderItem,OrderItemAdmin)

admin.site.register(OrderTracking)