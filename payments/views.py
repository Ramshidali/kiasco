# django
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# local
from main.decorators import role_required
from payments.models import Payment
from main.functions import decrypt_message, encrypt_message, get_auto_id, get_otp
# Create your views here.


# dashboard views
@login_required
@role_required(['superadmin'])
def payments(request):
    
    instances = Payment.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(order_id__icontains=query) |
            Q(payment_type__icontains=query) |
            Q(order_status__icontains=query) 
        )
        title = "Payment - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Payments',
        'page_title' : 'Payments',
        'filter_data' : filter_data,
    }
    
    return render(request, 'admin_panel/payments/payments.html', context)


@login_required
@role_required(['superadmin'])
def payment(request,pk):
    
    instance = Payment.objects.get(pk=pk, is_deleted=False)
    
    
    
    context = {
        'instance': instance,
        'page_name' : 'Payment',
        'page_title' : 'Payment',
        'is_need_light_box' : True,
            
    }
         
    return render(request, 'admin_panel/payments/payment.html', context)