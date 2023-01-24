import requests
#django
from django.db.models import Sum
#local
from customers.models import CartItem, Customer, WhishlistItem
from general.models import Contacts, Location
from orders.models import TempAddress
from product.models import ProductCategory

def main_context(request):
    is_customer = False
    customer = None
    location_status = False
    
    if Location.objects.filter(is_deleted=False).exists():
        if Location.objects.filter(is_deleted=False).count() == 2 :
            location_status = True

    categories = ProductCategory.objects.filter(is_deleted=False)
    contacts_detail = Contacts.objects.first()
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user).exists():
            customer = Customer.objects.get(user=request.user)
            is_customer = True

        wishlist = WhishlistItem.objects.filter(customer__user=request.user)
        wishlist_items = [item.product.pk for item in wishlist]

        cart = CartItem.objects.filter(customer__user=request.user,is_deleted=False)
        cart_items = [item.product_varient.product.pk for item in cart]

        cart_instance = CartItem.objects.filter(customer__user=request.user,is_deleted=False)
        cart_count = cart_instance.count()
        
        total_mrp = 0
        if CartItem.objects.filter(customer__user=request.user,is_deleted=False).exists():
            total_mrp = CartItem.objects.filter(customer__user=request.user,is_deleted=False).aggregate(total_price=Sum('unit_price'))["total_price"]
        total = total_mrp
        
        delivery_charge = 0
        if TempAddress.objects.filter(customer__user=request.user).exists():
            delivery_pincode = TempAddress.objects.get(customer__user=request.user).address.pincode
            
            baseurl_1 = f"https://api.postalpincode.in/pincode/{delivery_pincode}"
            postofficeapi_response = requests.get(baseurl_1).json()
            # print(postofficeapi_response,"reposne")
            # print(pincode)
            # print(type(baseurl_1))
            location = "other_state"
            if postofficeapi_response[0]["Status"] == 'Success' :
                if 'PostOffice' in postofficeapi_response[0] and 'postal_code':
                    for post_offices in postofficeapi_response[0]['PostOffice']:
                        response = post_offices
                        # print("Circle",response['Circle'])
                        # print("type",type(response))
                    response_list = list(response.values())[4]
                    response_list = [response_list]
                    # print("==========",type(response_list))
                    # print("==========",response_list)
                    for i in response_list:
                        if i == "Kerala" :
                            location = "kerala_state"
                        else:
                            location = "other_state"
            # print(location,"location")
            if Location.objects.filter(area=location,is_deleted=False).exists():
                delivery_charge = Location.objects.get(area=location,is_deleted=False).delivery_charge
            else:
                delivery_charge = 0
            # print(delivery_charge)
            
            # print(total_mrp,"charge")
            # print(delivery_charge,"delivery_charge")
            
            total = total_mrp+delivery_charge

        try:
            get_user_name = Customer.objects.get(user=request.user)
        except:
            get_user_name = ''


        return {
            'customer' : customer,
            'is_customer' : is_customer,

            'categories' : categories,

            'wishlist' : wishlist,
            'wishlist_items' : wishlist_items,

            'cart' : cart,
            'cart_items' : cart_items,

            'total_mrp' : total_mrp,
            'total_price' : total,
            'delivery_charge' : delivery_charge,
            'cart_count' : cart_count,

            'get_user_name' : get_user_name,

            'contacts_detail':contacts_detail,
            "location_status": location_status,
        }
    else:
        return {
            'categories' : categories,
            'contacts_detail':contacts_detail,
            "location_status": location_status,
        }