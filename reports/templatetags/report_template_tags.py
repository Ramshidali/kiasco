from django.template import Library

from orders.models import Order

register = Library()



@register.simple_tag(takes_context=True)
def get_total_orders(context, customer):
    
    total_orders = Order.objects.filter(is_deleted=False,customer=customer).count()
    return total_orders

@register.simple_tag(takes_context=True)
def get_completed_orders(context, customer):
    
    completed_orders = Order.objects.filter(is_deleted=False,order_status='delivered',customer=customer).count()
    return completed_orders

@register.simple_tag(takes_context=True)
def get_pending_orders(context, customer):
    
    pending_orders = Order.objects.filter(is_deleted=False,order_status='pending',customer=customer).count()
    return pending_orders

@register.simple_tag(takes_context=True)
def get_shipped_orders(context, customer):
    
    shipped_orders = Order.objects.filter(is_deleted=False,order_status='shipped',customer=customer).count()
    return shipped_orders