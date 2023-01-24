# django
from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import login_required
# local
from main.decorators import role_required
from  product.models import *
from orders.models import *
from payments.models import *
from customers.models import *
# Create your views here.


# dashboard views
@login_required
@role_required(['superadmin'])
def product_report(request):
    instances = ProductVariant.objects.filter(is_deleted=False).order_by("id")
        
    context = {
        'instances' : instances,
        'page_name' : 'Product Report',
        'page_title' : 'Product Report',
    }
 
    return render(request, 'admin_panel/reports/product_report.html', context)


@login_required
@role_required(['superadmin'])
def print_product_report(request):
    title = "Product Report"
    instances = ProductVariant.objects.filter(is_deleted=False).order_by('id')
        
    context = {
        "title": title,
        "instances": instances,

        "is_need_popup_box": True,
        "is_need_grid_system": True,
        "is_need_wave_effect": True,
        "is_need_select_picker": True,
        "is_need_chosen_select": True,
        "is_need_bootstrap_growl": True,
        "is_need_datetime_picker": True,
        "is_need_custom_scroll_bar": True,
    }

    return render(request, 'admin_panel/reports/product_report_print.html', context)


@login_required
@role_required(['superadmin'])
def order_report(request):
    instances = Order.objects.filter(is_deleted=False).order_by("id")
    
    context = {
        'instances' : instances,
        'page_name' : 'Order Report',
        'page_title' : 'Order Report',
    }
 
    return render(request, 'admin_panel/reports/order_report.html', context)



@login_required
@role_required(['superadmin'])
def print_order_report(request):
    title = "Order Report"
    instances = Order.objects.filter(is_deleted=False).order_by('id')
        
    context = {
        "title": title,
        "instances": instances,

        "is_need_popup_box": True,
        "is_need_grid_system": True,
        "is_need_wave_effect": True,
        "is_need_select_picker": True,
        "is_need_chosen_select": True,
        "is_need_bootstrap_growl": True,
        "is_need_datetime_picker": True,
        "is_need_custom_scroll_bar": True,
    }

    return render(request, 'admin_panel/reports/order_report_print.html', context)


@login_required
@role_required(['superadmin'])
def payment_report(request):
    instances = Order.objects.filter(is_deleted=False).order_by("id")
    
    context = {
        'instances' : instances,
        'page_name' : 'Payment Report',
        'page_title' : 'Payment Report',
    }
 
    return render(request, 'admin_panel/reports/payment_report.html', context)



@login_required
@role_required(['superadmin'])
def print_payment_report(request):
    title = "Payment Report"
    instances = Order.objects.filter(is_deleted=False).order_by('id')
    
    context = {
        "title": title,
        "instances": instances,

        "is_need_popup_box": True,
        "is_need_grid_system": True,
        "is_need_wave_effect": True,
        "is_need_select_picker": True,
        "is_need_chosen_select": True,
        "is_need_bootstrap_growl": True,
        "is_need_datetime_picker": True,
        "is_need_custom_scroll_bar": True,
    }

    return render(request, 'admin_panel/reports/payment_report_print.html', context)


@login_required
@role_required(['superadmin'])
def customer_report(request):
    instances = Customer.objects.filter(is_deleted=False).order_by("id")
    total_orders = Order.objects.filter(is_deleted=False,order_status='delivered').count()
    
    context = {
        'instances' : instances,
        'total_orders' : total_orders,
        'page_name' : 'Customer Report',
        'page_title' : 'Customer Report',
    }
 
    return render(request, 'admin_panel/reports/customer_report.html', context)



@login_required
@role_required(['superadmin'])
def print_customer_report(request):
    title = "Customer Report"
    instances = Customer.objects.filter(is_deleted=False).order_by('id')
    
    context = {
        "title": title,
        "instances": instances,

        "is_need_popup_box": True,
        "is_need_grid_system": True,
        "is_need_wave_effect": True,
        "is_need_select_picker": True,
        "is_need_chosen_select": True,
        "is_need_bootstrap_growl": True,
        "is_need_datetime_picker": True,
        "is_need_custom_scroll_bar": True,
    }

    return render(request, 'admin_panel/reports/customer_report_print.html', context)