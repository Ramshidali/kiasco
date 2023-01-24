#standard
import json
#django
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
#local
from main.decorators import role_required
from customers.models import Customer,CustomerAddress
from orders.models import * 

# Create your views here.


@login_required
@role_required(['superadmin'])
def customers(request):
    """
    customers listings
    :param request:
    :return: customer list view
    """
    instances = Customer.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) 
        )
        title = "Customer - %s" % query
        filter_data['q'] = query

    context = {
        'instances': instances,
        'page_name' : 'Customers',
        'page_title' : 'Customers',
        'filter_data' : filter_data
    }
    
    return render(request, 'admin_panel/customers/customers.html', context)


@login_required
@role_required(['superadmin'])
def customer(request,pk):
    """
    customer single view using customer pk
    :param request:
    :pk
    :return: customer list view
    """
    instance = Customer.objects.get(pk=pk, is_deleted=False)
    orders = OrderItem.objects.filter(order__customer=instance,is_deleted=False)
    
    print(orders)
    try:
        address = CustomerAddress.objects.filter(customer=instance)
        context = {
            'instance': instance,
            'address' :address,
            'page_name' : 'Customer',
            'page_title' : 'Customer',
            'is_need_light_box' : True,
            'orders' : orders
        }
    except:
        context = {
            'instance': instance,
            'page_name' : 'Customer',
            'page_title' : 'Customer',
            'is_need_light_box' : True,
            'orders' : orders
        }
         
    return render(request, 'admin_panel/customers/customer.html', context)


@login_required
@role_required(['superadmin'])
def revoke_customer(request, pk):
    auth_user = Customer.objects.get(pk=pk).user
    auth_user.is_active = False
    auth_user.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Revoked",
        "message": "Customer Successfully Revoked.",
        "redirect": "true",
        "redirect_url": reverse('customers:customer',kwargs={"pk":pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def grant_customer(request, pk):
    auth_user = Customer.objects.get(pk=pk).user
    auth_user.is_active = True
    auth_user.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Granted",
        "message": "Customer Access Granted.",
        "redirect": "true",
        "redirect_url": reverse('customers:customer',kwargs={"pk":pk})
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

