from datetime import datetime, timedelta
from email import message
from django import template
from customers.functions import get_user

from customers.models import CartItem, CustomerReview
from general.models import Location
from offers.models import Offers
from orders.models import Order, OrderItem, OrderTracking
from product.models import ProductVariant

register = template.Library()

@register.simple_tag
def get_cart_count(varient, user):
    if CartItem.objects.filter(product_varient__pk=varient, customer__user=user).exists():
        cart_item_instance = CartItem.objects.get(product_varient__pk=varient, customer__user=user,is_deleted=False)
        return cart_item_instance.qty
    else:
        return 1
    
    
@register.simple_tag
def get_order_delivery_date(order_id,product):
    
    if OrderItem.objects.get(order__pk=order_id,product_varient__product__pk=product).order_status == "pending" :
        print("insted in order is pending")
        
        if not OrderTracking.objects.filter(order__pk=order_id).exists():
            order_date = Order.objects.filter(pk=order_id).first().time.date()
            # print("hai",order_date)
            billing_pincode = Order.objects.filter(pk=order_id).first().billing_pincode
            delivery_date = Location.objects.get(pincode=billing_pincode).min_day_of_delivery
            
            expected_date = order_date + timedelta(days=delivery_date)
            expected_date = expected_date.strftime("%a, %b %d")
            
            message = "seller processing your order"            
            
            return {
                "text" : "delivery expected on ",
                "message" : message,
                "date" : expected_date,
                "class_name" : "delivery-date",
                }
        
        else:
            expected_date = OrderTracking.objects.get(order__pk=order_id).expected_date
            expected_date = expected_date.strftime("%a, %b %d")
                    
            return {
                "text" : "delivery expected on ",
                "message" : "seller processing your order",
                "class_name" : "delivery-date",
                "date" : expected_date,
                }
    
    elif OrderItem.objects.get(order__pk=order_id,product_varient__product__pk=product).order_status == "shipped" :
        
        message = "seller shipped your order"
        
        expected_date = OrderTracking.objects.get(order__pk=order_id).date_updated
        expected_date = expected_date.strftime("%a, %b %d")
        
        return {
            "text" : "Shipped on ",
            "message" : message,
            "date" : expected_date,   
            "class_name" : "delivery-date",
            }
    
    elif OrderItem.objects.get(order__pk=order_id,product_varient__product__pk=product).order_status == "delivered":
        # print("inserted into delivered if")
        
        delivery_date = OrderItem.objects.get(order__pk=order_id,product_varient__product__pk=product).date_updated
        delivery_date = delivery_date.strftime("%a, %b %d")
        
        
        return {
                "text" : "delivered on ",
                "date" : delivery_date,
                "status": "delivered",
                "class_name" : "delivery-date",
            }
    
    elif OrderItem.objects.get(order__pk=order_id,product_varient__product__pk=product).order_status == "cancelled":
        print("inserted into cancelled if")
        
        cancelled_date = OrderItem.objects.get(order__pk=order_id,product_varient__product__pk=product).date_updated
        cancelled_date = cancelled_date.strftime("%a, %b %d")
        
        
        return {
                "text" : "Cancelled on ",
                "date" : cancelled_date,
                "status": "cancelled",
                "class_name" : "cancelled-date",
            }
        

@register.simple_tag
def get_is_review(product, user):
    if CustomerReview.objects.filter(product_id=product, customer__user=user).exists():
        rating = CustomerReview.objects.get(product_id=product, customer__user=user)
        return {
            "status" : True,
            "rating" : rating.rating,
            }
    else:
        return {
            "status" : False,
            }
        

@register.simple_tag
def get_is_varient(product):
    if ProductVariant.objects.filter(product_id=product,stock__gt=0).exists():
        return True
    else:
        return False
    