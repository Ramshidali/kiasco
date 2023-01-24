# standerd
import json
import datetime
#django
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
#local
from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id,sendSMS
from orders.models import Order, OrderItem
from orders.forms import *
# Create your views here.


# dashboard views
@login_required
@role_required(['superadmin'])
def orders(request):
    instances = OrderItem.objects.filter(is_deleted=False).exclude(order__payment_status="failed").order_by("-date_added")
    
    if instances:
        for instance in instances:
            status= instance.order_status
            form = OrderStatusForm(initial={'order_status': status})
    else:
        form=OrderStatusForm()

    filter_data = {}
    query = request.GET.get("q")
    filter_query = request.GET.get('filter_query')

    if filter_query:
        if 'pending' in filter_query:
            instances = instances.filter(order_status="pending")

        elif 'shipped' in filter_query:
            instances = instances.filter(order_status="shipped")

        elif 'delivered' in filter_query:
            instances = instances.filter(order_status="delivered")

        elif 'cancelled' in filter_query:
            instances = instances.filter(order_status="cancelled")
    else:
        filter_query = 'all'

    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(order__customer__name__icontains=query)|
            Q(order__order_id__icontains=query)
        )
        title = "Order - %s" % query
        filter_data['q'] = query
        
    context = {
        'instances': instances,
        'page_name' : 'Orders',
        'page_title' : 'Orders',
        'filter_data' : filter_data,
        'filter_query' : filter_query,
        'form': form,
    }
  
    return render(request, 'admin_panel/orders/orders.html', context)


@login_required
@role_required(['superadmin'])
def order_item(request,pk):

    instance = OrderItem.objects.get(pk=pk, is_deleted=False)
    status= instance.order_status
    form = OrderStatusForm(initial={'order_status': status})
    tracking_form = OrderTrackingForm(initial={'order': instance})
    order_items = OrderItem.objects.filter(order=instance.order)
    
    try:
        instance_tracking = OrderTracking.objects.get(is_deleted=False,order=instance.order) 
        
        context = {
        'instance': instance,
        'order_items' :order_items,
        'page_name' : 'Orders',
        'page_title' : 'Orders',
        'form' :form,
        'tracking_form' :tracking_form,
        'instance_tracking' : instance_tracking,
        'is_need_light_box' : True,
    }
    except:
                
        context = {
            'instance': instance,
            'order_items' :order_items,
            'page_name' : 'Orders',
            'page_title' : 'Orders',
            'form' :form,
            # 'instance_tracking' : instance_tracking,
            'tracking_form' :tracking_form,
            'is_need_light_box' : True,
        }     
         
    return render(request, 'admin_panel/orders/order_item.html', context)


@login_required
@role_required(['superadmin'])
def change_order_status(request, pk):
    if request.method == 'POST':
        form = OrderStatusForm(request.POST)
        

        if form.is_valid():
            status = form.cleaned_data['order_status']
            date = datetime.datetime.today()
            OrderItem.objects.filter(pk=pk).update(order_status=status,date_updated=date)
            order = get_object_or_404(OrderItem, pk=pk).order
            tracking_details = OrderTracking.objects.get(order=order)
            time = datetime.date.today()
            

            message = None
            if status == "shipped":
                message = f"Dear KIASCO customer, your order {order.order_id} has been shipped with tracking ID {tracking_details.tracking_id} and will be expected by {str(tracking_details.expected_date)}."
                msg = sendSMS('shipped', order.customer.phone, [order.order_id, tracking_details.tracking_id ,str(tracking_details.expected_date) ])
                # print('\n\n-------------', msg, '-------------\n\n')

            elif status == "delivered":
                message = f"Dear KIASCO customer, your order {order.order_id} has been delivered on {str(time)}."  
                msg = sendSMS('delivered', order.customer.phone, [order.order_id, str(time)])
                # print('\n\n-------------', msg, '-------------\n\n')


            elif status == "cancelled":
                message = f"Dear KIASCO customer, your order {order.order_id} has been cancelled."
                msg = sendSMS('cancelled', order.customer.phone, [order.order_id])
                # print('\n\n-------------', msg, '-------------\n\n')
            
            # print(message)

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Order Status Successfully Updated.",
                "redirect": "true",
                "redirect_url": reverse('orders:order_item', kwargs={'pk':pk})
            }

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        
        
@login_required
@role_required(['superadmin'])
def add_tracking_details(request, pk):
    if request.method == 'POST':
        order = OrderItem.objects.get(pk=pk).order
        # print('ddddddddddddddddddddddddddddd',order)
        tracking_form = OrderTrackingForm(request.POST)

        if tracking_form.is_valid():
            data = tracking_form.save(commit=False)
            data.auto_id = get_auto_id(OrderTracking)
            data.creator = request.user
            data.updater = request.user
            data.order = order
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Added",
                "message": "Tracking Status Successfully Added.",
                "redirect": "true",
                "redirect_url": reverse('orders:order_item', kwargs={'pk':pk})
            }
         
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        
        else:
            message= generate_form_errors(tracking_form, formset=False)
            response_data = {
                "status": "error",
                "title": "Validation Error",
                "message": message
            }
    
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')