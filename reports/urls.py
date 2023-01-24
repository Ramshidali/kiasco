from django.urls import path, re_path
from . import views

app_name = 'reports'

urlpatterns = [
    re_path(r'^product-report/$', views.product_report, name='product_report'),
    re_path(r'^print-product-report/$', views.print_product_report, name='print_product_report'),
    
    re_path(r'^order-report/$', views.order_report, name='order_report'),
    re_path(r'^print-order-report/$', views.print_order_report, name='print_order_report'),
    
    re_path(r'^payment-report/$', views.payment_report, name='payment_report'),
    re_path(r'^print-payment-report/$', views.print_payment_report, name='print_payment_report'),
    
    re_path(r'^customer-report/$', views.customer_report, name='customer_report'),
    re_path(r'^print-customer-report/$', views.print_customer_report, name='print_customer_report'),
]