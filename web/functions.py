from django.conf import settings    
from django.contrib.auth.models import User
from general.models import Location
import requests
import http.client




def sendSMS(numbers, message):
    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = "{\"flow_id\":\"607d53323daf4e0f9b3a6d12\",\"sender\":\"fashup\",\"mobiles\":\"91%s\",\"var\":\"%s\"}" %(numbers,message)
    
    headers = {
        'authkey': "353156AGnT1CbUjivF6017ec84P1",
        'content-type': "application/JSON"
        }

    conn.request("POST", "/api/v5/flow/", payload, headers)
    
    res = conn.getresponse()
    print(res,"=========================")
    data = res.read()


def get_current_location(request):
    choosed_location = None
    is_customer_exist , customer = check_customer(request)

    if "choosed_location" in request.session:
        pk =  request.session['choosed_location']

        if Location.objects.filter(is_deleted=False,pk=pk).exists():
            choosed_location = Location.objects.get(is_deleted=False,pk=pk)

    elif is_customer_exist:
        if customer.location:
            pk = customer.location.pk
            if Location.objects.filter(is_deleted=False,pk=pk).exists():
                choosed_location = Location.objects.get(is_deleted=False,pk=pk)

        else:
            if Location.objects.filter(is_deleted=False,name__iexact="Pan India").exists():
                choosed_location = Location.objects.filter(is_deleted=False,name__iexact="Pan India").latest("id")
    else:    
        if Location.objects.filter(is_deleted=False,name__iexact="Pan India").exists():
            choosed_location = Location.objects.filter(is_deleted=False,name__iexact="Pan India").latest("id")

        else:

            if Location.objects.filter(is_deleted=False).exists():
                choosed_location = Location.objects.filter(is_deleted=False).latest("id")

    if choosed_location == None:
        if Location.objects.filter(is_deleted=False).exists():
            choosed_location = Location.objects.filter(is_deleted=False).latest("id")
         
    return choosed_location

def get_current_category(request):
    current_vendor_category = VendorCategory.objects.none()
    is_customer_exist , customer = check_customer(request)

    if "current_vendor_category" in request.session:
        
        pk =  request.session['current_vendor_category']
        if pk == 'all':
            if VendorCategory.objects.filter(is_deleted=False).exists():
                current_vendor_category = VendorCategory.objects.filter(is_deleted=False)
        else:
            if VendorCategory.objects.filter(is_deleted=False,pk=pk).exists():
                current_vendor_category = VendorCategory.objects.filter(is_deleted=False,pk=pk)
    else:
        if VendorCategory.objects.filter(is_deleted=False).exists():
            current_vendor_category = VendorCategory.objects.filter(is_deleted=False)   
       
    return current_vendor_category.values_list('pk',flat=True)