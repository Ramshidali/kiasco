#standerd
from email import message
import json
import datetime
import requests
#django
from django.db.models import Q,F
from django.http import JsonResponse
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.conf import settings as SETTINGS
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
#thirdparty
from datetime import datetime
from datetime import timedelta
import razorpay
#local
from customers.models import CartItem, Customer, CustomerAddress, CustomerReview, OtpEmailRecords, OtpRecords, WhishlistItem
from general.models import Location
from main.functions import decrypt_message, encrypt_message, generate_form_errors, get_auto_id, get_otp, get_user, paginate, send_email,sendSMS
from orders.models import Order, OrderItem, TempAddress
from payments.models import Payment
from product.models import Product, ProductCategory, ProductImage, ProductSizeChart, ProductVariant, SizeMeasurementChart
from web.forms import AboutCustomerReviewForm, AboutDescriptionForm, AboutGalleryForm, AddressForm, BannersForm, CancelReasonForm, RatingForm
from web.models import AboutCustomerReview, AboutDescription, AboutGallery, Banner
from django.template.context_processors import csrf

client = razorpay.Client(auth=("rzp_live_JeBmeKCs93Z4h0", "9576y9uExlEQSUUj0WUkqW0z"))



def index(request):

    instances = ProductCategory.objects.filter(is_deleted=False)
    banner_instances = Banner.objects.filter(is_deleted=False)

    context = {
        'instances' : instances,
        'banner_instance' : banner_instances,
        'page_name' : 'Home',
        'is_home' : True,
        'home' : True,
    }

    return render(request,'web/index.html', context)


# create and update otp by phone number
def otp_generation(request):
    phone = request.GET.get("phone")
    otp = get_otp()

    response_data = {}

    if phone:
        if len(phone) == 10:
            if OtpRecords.objects.filter(phone=phone).exists():
                OtpRecords.objects.filter(phone=phone).update(
                    otp=str(otp),
                )
                if User.objects.filter(username=phone).exists():
                    user = User.objects.get(username=phone)
                    user.set_password(otp)
                    user.save()

                    Customer.objects.filter(phone=phone).update(password=encrypt_message(otp))

                message = f"Dear customer, {otp} is your OTP from KIASCO. Don't share your OTP with anyone."
                msg = sendSMS('otp', phone, [otp])
                # print('\n\n-------------', msg, '-------------\n\n')

                # print(message)

                response_data = {
                    "status": "true",
                }

            else:
                message = f"Dear customer, {otp} is your OTP from KIASCO. Don't share your OTP with anyone."
                msg = sendSMS('otp', phone, [otp])
                # print('\n\n-------------', msg, '-------------\n\n')

                # print(message)

                otp_data = OtpRecords.objects.create(
                    phone=phone,
                    otp=otp,
                )
                response_data = {"status": "true",}

        else:
            response_data = {
                "status": 'number_not_valid',
                "message": "Please enter your 10 digit mobile number without space and don't add 91 or 0 or +91 before your number"
            }

    else:
        response_data = {"status": "6001"}

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# varify phone otp
def verify_otp(request):
    response_data = {}

    otp_one = request.GET.get("otp_one")
    otp_two = request.GET.get("otp_two")
    otp_three = request.GET.get("otp_three")
    otp_four = request.GET.get("otp_four")

    phone = request.GET.get("phone")

    otp_final = otp_one + otp_two + otp_three + otp_four

    # print(phone, otp_final,"---otp_final")

    if otp_final:
        if OtpRecords.objects.filter(phone=phone).exists():
            if OtpRecords.objects.filter(phone=phone, otp=otp_final).exists():
                otp_show = OtpRecords.objects.get(phone=phone)

                response_data = {
                    "status": "true",
                    "phone": phone,
                }

            else:
                response_data = {
                    "status": "false",
                    "condition_status" : "not_match",
                    "message": "otp not match please enter otp",
                }

        else:
            response_data = {
                "status": "phone number not exist"
            }

    else:
        print("varify error")

        response_data = {
            "status": "false"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def customer_join(request):
    response_data = {}
    phone =  request.GET.get("phone")
    otp_one = request.GET.get("otp_one")
    otp_two = request.GET.get("otp_two")
    otp_three = request.GET.get("otp_three")
    otp_four = request.GET.get("otp_four")

    otp =  otp_one + otp_two + otp_three + otp_four

    if OtpRecords.objects.filter(phone=phone,otp=otp).exists():
        if User.objects.filter(username=phone).exists():
            user = authenticate(username=phone, password=otp)
            if user is not None:
                login(request,user)

                response_data = {
                    "status": 'true',
                    "next_action": "exit",
                    }
        else:
            # name = request.GET.get("user_name")
            # email = request.GET.get("email")
            # gender = request.GET.get("gender")

            # user_data = User.objects.create_user(
            #     username=email,
            #     email=email,
            #     password=otp,
            #     is_active=True,
            # )
            # # print(user_data,'printedddd')

            # if Group.objects.filter(name="customer_user").exists():
            #     group = Group.objects.get(name="customer_user")
            # else:
            #     group = Group.objects.create(name="customer_user")

            # user_data.groups.add(group)

            # Customer.objects.create(
            #     user=user_data,
            #     auto_id=get_auto_id(Customer),
            #     creator=user_data,
            #     updater=user_data,
            #     name=name,
            #     phone=phone,
            #     password=encrypt_message(otp),
            #     email=email,
            #     gender=gender,
            # )
            # user = authenticate(username=email, password=otp)
            # if user is not None:
            #     login(request,user)

            # response_data = {
            #     "status": 'true'
            # }

            response_data = {
                "status": "true",
                "phone" : phone,
                "next_action": "registration_page",
                }
    else:
        message = "otp not match please enter otp"

        response_data = {
            "status": "false",
            "condition_status" : "not_match",
            "message": message,
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# signup using phone number
def signup(request):
    phone = request.GET.get("phone")
    name = request.GET.get("user_name")
    email = request.GET.get("email")
    gender = request.GET.get("gender")

    otp = OtpRecords.objects.get(phone=phone).phone

    user_data = User.objects.create_user(
        username=phone,
        email=email,
        password=otp,
        is_active=True,
    )
    # print(user_data,'printedddd')

    if Group.objects.filter(name="customer_user").exists():
        group = Group.objects.get(name="customer_user")
    else:
        group = Group.objects.create(name="customer_user")

    user_data.groups.add(group)

    Customer.objects.create(
        user=user_data,
        auto_id=get_auto_id(Customer),
        creator=user_data,
        updater=user_data,
        name=name,
        phone=phone,
        password=encrypt_message(otp),
        email=email,
        gender=gender,
    )
    user = authenticate(username=phone, password=otp)
    if user is not None:
        login(request,user)

    response_data = {
        "status": 'true',
        "next_action": "exit",
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# old sign up using email and password
# def customer_signup(request):

#     phone = request.GET.get("phone")
#     name = request.GET.get("user_name")
#     email = request.GET.get("email")
#     password = request.GET.get("password")
#     gender = request.GET.get("gender")

#     response_data = {}

#     if phone and name and email and password and gender:
#         if len(phone) == 10:
#             if Customer.objects.filter(phone=phone).exists():
#                 # print("phone=phone")
#                 response_data = {
#                     "status": '6001',
#                     'condition_status' : "phone_already_exists",
#                     "message": "This Phone Number already exists"
#                     }
#             else :

#                 if User.objects.filter(email=email).exists():
#                     # print("email=email")
#                     response_data = {
#                     "status": '6001',
#                     'condition_status' : "email_already_exists",
#                     "message": "This email id already used"
#                     }

#                 else:
#                     if OtpRecords.objects.filter(phone=phone).exists():

#                         user_data = User.objects.create_user(
#                             username=email,
#                             email=email,
#                             password=password,
#                             is_active=True,
#                         )
#                         # print(user_data,'printedddd')

#                         if Group.objects.filter(name="customer_user").exists():
#                             group = Group.objects.get(name="customer_user")
#                         else:
#                             group = Group.objects.create(name="customer_user")

#                         user_data.groups.add(group)

#                         Customer.objects.create(
#                             user=user_data,
#                             auto_id=get_auto_id(Customer),
#                             creator=user_data,
#                             updater=user_data,
#                             name=name,
#                             phone=phone,
#                             password=encrypt_message(password),
#                             email=email,
#                             gender=gender,
#                         )
#                         user = authenticate(username=email, password=password)
#                         if user is not None:
#                             login(request,user)

#                             # print('true')

#                         response_data = {
#                             "status": 'true'
#                         }
#                     else:
#                         # print('alreay exist')
#                         response_data = {
#                             "status": '6001',
#                             'condition_status' : 'user_already_exists',
#                             "message": "User already exists"
#                         }


#         else:
#             response_data = {
#                 "status": '6001',
#                 'condition_status' : "phone_number_not_currect",
#                 "message": "Please enter your 10 digit mobile number without space and don't add 91 or 0 or +91 before your number"
#             }
#     else:
#         # print("fill all fields")

#         response_data = {
#             "status": 'false'
#         }

#     return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# def customer_signin(request):
#     # print("in view")

#     email = request.GET.get("email")
#     password = request.GET.get("password")

#     response_data = {}

#     if email and password:
#         # print("email and password")

#         if User.objects.filter(username=email).exists():
#             # print("user")
#             user = User.objects.get(username=email)

#             customer = Customer.objects.get(user=user)
#             customer_pass = decrypt_message(customer.password)
#             # print(customer_pass,"c_passsssssssss")
#             # print(password,"passsssssssss")

#             if password==customer_pass:
#                 user = authenticate(username=email, password=password)

#                 # print(user,"user-------------   ")
#                 # print(request.user,"request-----")
#                 # print(customer_pass,"cst pass ----------")
#                 # print(email,"emailllllllllllllllll")


#                 if user is not None:
#                     login(request,user)

#                     # print(customer_pass,"cusssssssssssssssss")
#                     # print("user loging successfull")
#                     # print(user)

#                     response_data = {
#                         "status": "true"
#                     }
#             else:
#                 # print("username and password not match")
#                 response_data = {
#                     "status": "false",
#                     "condition_status" : "password_not_match",
#                     "message" : "username and password not match",
#                 }
#         else:
#             # print("user not found")
#             response_data = {
#                 "status": "false",
#                 "condition_status" : "username_not_found",
#                 "message" : "username and password not found,please signup or check email",
#             }
#     else:
#         # print("no pass no user")
#         response_data = {
#             "status": "6001"
#         }

#     return HttpResponse(json.dumps(response_data), content_type='application/javascript')

def customer_logout(request):
    logout(request)
    context = {

    }

    return redirect(reverse('web:index'))


# forgot password user checking and otp send to email id
def check_user(request):
    response_data = {}

    otp = get_otp()
    email = request.GET.get("email")

    if User.objects.filter(username=email).exists():

        if OtpEmailRecords.objects.filter(email=email).exists():
            OtpEmailRecords.objects.filter(email=email).update(
                otp=str(otp),
            )
            # print("otp updated")

            message = f"Dear customer, {otp} is your OTP from KIASCO. Don't share your OTP with anyone."
            # msg = sendSMS('otp', phone, [otp])
            # print('\n\n-------------', msg, '-------------\n\n')

            # print(message)

        else:
            message = f"Dear customer, {otp} is your OTP from KIASCO. Don't share your OTP with anyone."
            # msg = sendSMS('otp', phone, [otp])
            # print('\n\n-------------', msg, '-------------\n\n')

            # print(message)

            otp_data = OtpEmailRecords.objects.create(
                email=email,
                otp=otp,
            )
        send_email("Kiasco user varification",email,message)

        response_data = {
            "status": "true"
            }

    else:
        response_data = {
            "status" : "false",
            "message" : "user not found, please signup or check email"
            }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

# varify email otp
def verify_email_otp(request):

    otp_one = request.GET.get("otp_one")
    otp_two = request.GET.get("otp_two")
    otp_three = request.GET.get("otp_three")
    otp_four = request.GET.get("otp_four")

    # print(otp_one)
    # print(otp_two)
    # print(otp_three)
    # print(otp_four)

    email = request.GET.get("email")

    otp_final = otp_one + otp_two + otp_three + otp_four

    response_data = {}

    if otp_final:

        if OtpEmailRecords.objects.filter(email=email).exists():
            # print("First if")
            if OtpEmailRecords.objects.filter(email=email, otp=otp_final).exists():
                otp_show = OtpEmailRecords.objects.get(email=email)
                # print(otp_show.otp,"testttttttttttttttttststststst")
                response_data = {
                    "status": "true"
                }

            else:
                # otp error
                response_data = {
                    "status": "false",
                    "condition_status" : "not_match",
                    "message": "otp not match please enter otp",
                }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def forgot_password(request):
    response_data = {}
    email = request.GET.get("email")
    password = request.GET.get("password")
    c_password = request.GET.get("c_password")

    user = get_object_or_404(User.objects.filter(username=email))
    customer_instance = Customer.objects.filter(user=user)

    if password == c_password :
        # print("new and c password true")
        user.set_password(password)
        user.save()

        # print("user pass save")

        customer_instance.update(
            password=encrypt_message(password)
            )

        response_data = {
            "status": "true",
            "message" : "password changing successfully completed",
        }

    else:
        response_data = {
        "status": "false",
        "condition_status" : "password_not_match ",
        "message" : "new password and confirm password not match",
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def product_view(request,pk):
    instance = Product.objects.get(pk=pk, is_deleted=False)
    persentage = (instance.mrp - instance.price)/instance.mrp * 100
    product_variant = ProductVariant.objects.filter(product__pk=instance.pk,stock__gt = 0,is_deleted=False)
    more_images = ProductImage.objects.filter(product__pk=instance.pk,is_deleted=False)

    more_products = Product.objects.filter(category__pk=instance.category.pk,is_deleted=False).exclude(pk=instance.pk)

    if ProductSizeChart.objects.filter(Product_type=instance.product_type,is_deleted=False).exists():
        size_chart_instance = ProductSizeChart.objects.filter(Product_type=instance.product_type,is_deleted=False)
    else:

        size_chart_instance = ""

    if SizeMeasurementChart.objects.filter(product_type=instance.product_type).exists():
        size_image_instance = SizeMeasurementChart.objects.filter(product_type=instance.product_type).first()
        # print("inifiiiiiiiiiiiiiiiiiiiiiiiii")
    else:
        # print("inifiiiiiiiiiiiiiiiiiiiiiiiiielsess")
        size_image_instance = ""

    ratings = CustomerReview.objects.filter(product__pk=instance.pk,is_deleted=False)

    total_ratings = ratings.aggregate(Sum('rating')).get('rating__sum')

    if total_ratings == None:
        total_ratings = 0

    # print(total_ratings,"rattttttinnngnggn total")
    total_rating = ratings.count()

    try:
        current_rating = total_ratings / ratings.count()
        five_star_percentage = round((ratings.filter(rating=5).count() / total_rating) * 100, 1)
        four_star_percentage = round((ratings.filter(rating=4).count() / total_rating) * 100, 1)
        three_star_percentage = round((ratings.filter(rating=3).count() / total_rating) * 100, 1)
        two_star_percentage = round((ratings.filter(rating=2).count() / total_rating) * 100, 1)
        one_star_percentage = round((ratings.filter(rating=1).count() / total_rating) * 100, 1)

    except ZeroDivisionError:
        current_rating = 0
        five_star_percentage = 0
        four_star_percentage = 0
        three_star_percentage = 0
        two_star_percentage = 0
        one_star_percentage = 0

    # print(five_star_percentage)
    # print(four_star_percentage)
    # print(three_star_percentage)
    # print(two_star_percentage)
    # print(one_star_percentage)


    context = {
        'instance': instance,
        'featured_image': instance.featured_image.url,
        'persentage' : int(persentage),
        'product_variant' : product_variant,
        'more_images' : more_images,
        'more_products' : more_products,
        'size_chart' : size_chart_instance,
        'size_chart_img' : size_image_instance,

        'review' : ratings,

        'five_star': ratings.filter(rating=5).count(),
        'five_star_percentage': five_star_percentage,

        'four_star': ratings.filter(rating=4).count(),
        'four_star_percentage': four_star_percentage,

        'three_star': ratings.filter(rating=3).count(),
        'three_star_percentage': three_star_percentage,

        'two_star': ratings.filter(rating=2).count(),
        'two_star_percentage': two_star_percentage,

        'one_star': ratings.filter(rating=1).count(),
        'one_star_percentage': one_star_percentage,

        'current_rating': round(current_rating, 1),
        'total_rating': total_rating,

        'page_name' : instance.category.name,
        'page_title' : instance.category.name,

        'is_product_single' : True,
    }

    return render(request, 'web/pages/product.html', context)


def check_varient(request):
    response_data = {}
    pk = request.GET.get("brand_pk")
    try :
        if CartItem.objects.filter(customer__user=request.user,product_varient=pk,is_deleted=False).exists():

            response_data = {
                "status": "true",
                }

        else:
            response_data = {
                "status" : "false",
            }
    except:
        response_data = {
                "status" : "false",
            }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')




def show_all_product(request,pk):
    instances = Product.objects.filter(category__pk=pk, is_deleted=False)
    category_name = ProductCategory.objects.get(pk=pk,is_deleted=False)

    sort_query = request.GET.get("product_filter")

    if sort_query:
        if 'highest' in sort_query:
            instances = Product.objects.filter(category__pk=pk, is_deleted=False).order_by('-price')

        elif 'lowest' in sort_query:
            instances = Product.objects.filter(category__pk=pk, is_deleted=False).order_by('price')

        elif 'recommended' in sort_query:
            instances = Product.objects.filter(category__pk=pk, is_deleted=False).order_by('-current_rating')


    context = {
        'instances': paginate(instances, request),
        'category_name' : category_name,
        'is_category' : True,
        'sort_query' : sort_query,

        'page_name' : 'Products',
        'page_title' : 'Products',
        'is_category' : True,
        'category_pk' : pk
    }

    return render(request, 'web/pages/products_list.html', context)


def shop(request):
    """
    product view (all products)
    :param request:
    """
    instances = Product.objects.filter(is_deleted=False)
    category_name = ProductCategory.objects.filter(is_deleted=False)

    query = request.GET.get("q")
    sort_query = request.GET.get("product_filter")
    filter_data = {}

    if sort_query:
        if 'highest' in sort_query:
            instances = Product.objects.filter(is_deleted=False).order_by('-price')

        elif 'lowest' in sort_query:
            instances = Product.objects.filter(is_deleted=False).order_by('price')

        elif 'recommended' in sort_query:
            instances = Product.objects.filter(is_deleted=False).order_by('-current_rating')

        else:
            instances = Product.objects.filter(is_deleted=False,category__pk=sort_query)


    if query:

        instances = instances.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(product_type__icontains=query) |
            Q(meta_keywords__name__icontains=query)
        )
        filter_data['q'] = query


    context = {
        'instances': paginate(instances, request),
        'filter_data' : filter_data,
        'sort_query' : sort_query,
        'page_name' : 'Products',
        'page_title' : 'Product Details',
        'is_shop' : True,
        'is_category' : True,
        'category_name' : category_name,
    }

    return render(request, 'web/pages/products_list.html', context)

def new_collection(request):
    """
    new collection products view
    :param request:
    """
    instances = Product.objects.filter(is_deleted=False).order_by('-date_added')
    category_name = ProductCategory.objects.filter(is_deleted=False)

    sort_query = request.GET.get("product_filter")

    if sort_query:
        if 'highest' in sort_query:
            instances = Product.objects.filter(is_deleted=False).order_by('-price')

        elif 'lowest' in sort_query:
            instances = Product.objects.filter(is_deleted=False).order_by('price')

        elif 'recommended' in sort_query:
            instances = Product.objects.filter(is_deleted=False).order_by('-current_rating')

        else:
            instances = Product.objects.filter(is_deleted=False,category__pk=sort_query)

    context = {
        'instances': paginate(instances, request),
        'sort_query' : sort_query,

        'page_name' : 'Products',
        'page_title' : 'New Collection',
        'is_new' : True,
        'is_category' : True,
        'category_name' : category_name,
    }

    return render(request, 'web/pages/new-collection.html', context)


def add_to_wishlist(request):
    product = request.GET.get('product')
    product_instance = Product.objects.get(pk=product)

    response_data = {}

    if request.user.is_authenticated and not request.user.is_superuser:
        # print(request.user)
        customer = get_user(request.user)
        # Wishlistitem check
        if WhishlistItem.objects.filter(product=product_instance, customer=customer).exists():
            remove = WhishlistItem.objects.filter(product=product_instance,customer=customer)
            remove.delete()
            # print("remove")
            response_data = {
                "status": "removed"
            }
        else:
            WhishlistItem.objects.create(
                product=product_instance,
                customer=customer
            )
            response_data = {
                "status": "added"
            }
    else:
        response_data = {
            "status": "nouser"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def view_wishlist(request):
    """
    wishlist products view
    :param request:
    """
    if request.user.is_authenticated and not request.user.is_superuser :
        # print("in if***********************")
        customer = get_user(request.user)
        instances = WhishlistItem.objects.filter(customer=customer).order_by('-id')
        counts = WhishlistItem.objects.filter(customer=customer).count()
        # print("====>>>",instances)


        context = {
            'instances': paginate(instances, request),
            'counts' : counts,

            'page_name' : 'My Wishlist',
            'page_title' : 'New Collection',
        }

        return render(request, 'web/pages/wishlist.html', context)

    else:
        context = {
            'page_name' : 'My Wishlist',
            'page_title' : 'New Collection',
        }

        return render(request, 'web/pages/wishlist.html', context)


def view_cart(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        customer = get_user(request.user)
        instances = CartItem.objects.filter(customer=customer,is_deleted=False).order_by('date_added')
        counts = instances.count()

        # for i in instances:
        #     print(i.unit_price,"----unit_price")

        total = instances.aggregate(total_price=Sum('unit_price'))["total_price"]

        # print(total ,"-------total", counts,"--counts")

        if total:
            total = str(total)
        else:
            total = 0

        context = {
            'instances': paginate(instances, request),
            'total_items' : counts,
            'total' : total,

            'page_name' : 'Cart',
        }

        return render(request, 'web/pages/cart.html', context)

    else:
        context = {
            'page_title' : 'Cart',
        }

        return render(request, 'web/pages/cart.html', context)


def add_to_cart(request):
    product_varient = request.GET.get('varient')
    # print(product_varient)
    product_varient = ProductVariant.objects.get(pk=product_varient)

    response_data = {}

    if request.user.is_authenticated and not request.user.is_superuser:
        # print(request.user)
        customer = get_user(request.user)
        # Wishlistitem check
        if CartItem.objects.filter(product_varient=product_varient, customer=customer, is_deleted=False).exists():

            response_data = {
                "status": "allredy in cart"
            }
        else:
            CartItem.objects.create(
                product_varient=product_varient,
                customer=customer,
                auto_id = get_auto_id(CartItem),
                creator = request.user,
                date_updated = datetime.today(),
                updater = request.user,
                unit_price = product_varient.product.current_price()
            )
            # print("added to cart")
            response_data = {
                "status": "added"
            }
    else:
        # print("nouser")
        response_data = {
            "status": "nouser"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def remove_from_cart(request):
    # print("looooooloolololo")
    product_varient = request.GET.get('varient')
    # print(product_varient)
    pro_varient_instance = ProductVariant.objects.get(pk=product_varient)

    response_data = {}

    if request.user.is_authenticated and not request.user.is_superuser:
        # print(request.user)
        customer = get_user(request.user)


        if CartItem.objects.filter(product_varient=pro_varient_instance, customer=customer, is_deleted=False).exists():
            CartItem.objects.filter(
                product_varient=pro_varient_instance,
                customer=customer).delete()

            # print("remove")
            response_data = {
                "status": "true",
                "action" : "removed",
                "title": "Successfully Deleted",
                "message": "Product Successfully Deleted.",
                "redirect": "true",
                "redirect_url": reverse('web:increment_cart')
            }
        else:
            # print("no varient")
            response_data = {
            "status": "no varient in cart"
        }
    else:
        # print("nouser")
        response_data = {
            "status": "nouser"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def increment_cart(request):
    varient = request.GET.get('product_variant')
    customer = get_user(request.user)
    varient_instance = ProductVariant.objects.get(pk=varient)
    product = varient_instance.product.pk

    today = datetime.today()

    response_data = {}

    if CartItem.objects.filter(product_varient=varient_instance, customer=customer, is_deleted=False).exists():
        cart_item_instance = CartItem.objects.get(product_varient=varient_instance, customer=customer, is_deleted=False)
        cart_item_instance.qty = cart_item_instance.qty + 1

        price = cart_item_instance.product_varient.product.current_price()

        stock = varient_instance.stock

        # print(stock)
        # print(cart_item_instance.qty)


        if cart_item_instance.qty > stock :

            response_data = {
            "status": "greaterthan",
            "message" : "only " + str(stock) + " stocks are available",
        }

        else:
            # print("else")

            product_price = price * cart_item_instance.qty

            cart_item_instance.unit_price = product_price
            cart_item_instance.save()

            total = CartItem.objects.filter(customer__user=request.user).aggregate(total_price=Sum('unit_price'))["total_price"]

            response_data = {
                "status": "updated",
                "qty": cart_item_instance.qty,
                "unit_price" : float(cart_item_instance.unit_price),
                "total_price" : float(total),
            }
    else:

        response_data = {
            "status": "eroor"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def decrement_cart(request):
    varient = request.GET.get('product_variant')
    customer = get_user(request.user)
    varient_instance = ProductVariant.objects.get(pk=varient)
    product = varient_instance.product.pk

    today = datetime.today()

    response_data = {}

    if CartItem.objects.filter(product_varient=varient_instance, customer=customer, is_deleted=False).exists():
        cart_item_instance = CartItem.objects.get(product_varient=varient_instance, customer=customer, is_deleted=False)
        cart_item_instance.qty = cart_item_instance.qty - 1

        price = cart_item_instance.product_varient.product.current_price()

        product_price = price * cart_item_instance.qty


        if cart_item_instance.qty == 0:
            # print('-------------',cart_item_instance)
            # CartItem.objects.filter(pk=cart_item_instance.pk).delete()

            # print("qty one")

            response_data = {
                "status": "true",
                "qty": 0,
            }
        else:

            cart_item_instance.unit_price = product_price
            cart_item_instance.save()

        total = CartItem.objects.filter(customer__user=request.user).aggregate(total_price=Sum('unit_price'))["total_price"]

        response_data = {
            "status": "updated",
            "qty": cart_item_instance.qty,
            "price" : float(product_price),
            "unit_price" : float(cart_item_instance.unit_price),
            "total_price" : float(total),
        }
    else:

        response_data = {
            "status": "eroor"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def check_pincode(request):
    """
    check pincode using pincode
    :param request:
    """
    pincode = request.GET.get('pincode')
    baseurl_1 = f"https://api.postalpincode.in/pincode/{pincode}"
    postofficeapi_response = requests.get(baseurl_1).json()
    # print(postofficeapi_response,"reposne")
    # print(pincode)
    # print(type(baseurl_1))

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
            if response_list == "Kerala" :
                location = "kerala_state"
                # delivery_charge =
            else:
                location = "other_state"

    # print (location)

    pincode_check = Location.objects.filter(pincode=pincode).exists()

    response_data = {}

    if pincode_check :
        data_location = Location.objects.filter(pincode=pincode).first()

        min_date = datetime.today() + timedelta(days=data_location.min_day_of_delivery)
        min_date = min_date.strftime("%a, %b %d")
        # print("available")
        # print(data_location.delivery_charge,"del-charge")
        # print(data_location.cash_on_delivery,"cash on delivery")
        # print(data_location.min_day_of_delivery,"min day of delivery")
        # print(min_date.date(),"min_date")
        # print(min_date.strftime("%a, %b %d"))

        response_data = {
            "status": "available",

            "delivery_charge": str(data_location.delivery_charge),
            "delivery_date": min_date,
        }
    else:

        response_data = {
            "status": "available",

            "delivery_charge": str(0),
            "delivery_date": 0,
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def profile(request):
    if request.user.is_authenticated and not request.user.is_superuser:

        profile_instance = Customer.objects.get(user=request.user)

        context = {
            "profile_instance": profile_instance,
            "is_profile" : True,
            'page_name' : 'Profile',
        }

        return render(request, 'web/pages/edit-profile.html',context)

    else:

        return HttpResponseRedirect(reverse('web:dashboard', ))


def change_profile_details(request):
    response_data = {}
    # new_phone = request.GET.get('new_phone')
    full_name = request.GET.get('c_name')
    old_mail = request.user.email
    email = request.GET.get('email')
    gender = request.GET.get('gender')

    if request.user.is_authenticated and not request.user.is_superuser:
        Customer.objects.filter(user=request.user).update(
            name=full_name,
            email=email,
            gender=gender,
            )

        if old_mail != email:
            User.objects.filter(username=old_mail).update(
                username=email,
                email=email,
                )


        response_data = {
            "status": "success"
        }

    else:
        response_data = {
            "status": "nouser"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# change phone number section from pofile edit page
def generate_phone_otp(request):
    phone = Customer.objects.get(user=request.user, is_deleted=False).phone
    otp = get_otp()

    response_data = {}

    if phone:
        if len(phone) == 10:

            if OtpRecords.objects.filter(phone=phone).exists():
                OtpRecords.objects.filter(phone=phone).update(
                    otp=str(otp),
                )
                print("otp updated")


                message = f"Dear customer, {otp} is your OTP from KIASCO. Don't share your OTP with anyone."
                # msg = sendSMS('otp', phone, [otp])
                print(message)
                print("test cheyy")

                response_data = {
                    "status": "true",
                    "phone" : phone,
                }

                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            else:
                message = f"Dear customer, {otp} is your OTP from KIASCO. Don't share your OTP with anyone."
                # msg = sendSMS('otp', phone, [otp])
                print(message)

                otp_data = OtpRecords.objects.create(
                    phone=phone,
                    otp=otp,
                )
                print("otp created")
                response_data = {
                    "status": "true",
                    "phone" : phone,
                }

        else:
            print("phone mor than 10")
            response_data = {
                "status": 'number_not_valid',
                "message": "Please enter your 10 digit mobile number without space and don't add 91 or 0 or +91 before your number"
            }

    else:
        response_data = {
            "status": "6001"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



def change_phone_number(request):
    response_data = {}
    if request.user.is_authenticated and not request.user.is_superuser:

        old_phone = Customer.objects.get(user=request.user, is_deleted=False).phone
        new_phone = request.GET.get('new_phone')

        Customer.objects.filter(user=request.user).update(
            phone=new_phone,
            )

        OtpRecords.objects.filter(phone=old_phone).update(
            phone=new_phone,
            )

        response_data = {
            "status": "true"
        }

    else:
        response_data = {
            "status": "nouser"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def change_password(request):
    response_data = {}
    # print("inserted in change password")


    if request.user.is_authenticated and not request.user.is_superuser:
        # print("have user")

        pk = request.user.pk
        user = get_object_or_404(User.objects.filter(pk=pk))

        old_password = request.GET.get('old_password')
        new_password = request.GET.get('new_password')
        c_password = request.GET.get('c_password')

        customer_instance = Customer.objects.filter(user=user)
        # decrypted_pass = decrypt_message(customer_instance.password)

        if user.check_password(old_password):
            # print("user password true")

            if new_password == c_password :
                # print("new and c password true")
                user.set_password(new_password)
                user.save()

                # print("user pass save")

                customer_instance.update(
                    password=encrypt_message(new_password)
                    )

                response_data = {
                    "status": "success",
                    "message" : "password changing successfully completed",
                }
            else:
                response_data = {
                "status": "false",
                "condition_status" : "new_and_confirm_password_not_match ",
                "message" : "new password and confirm password not match",
            }
        else:
            response_data = {
            "status": "false",
            "condition_status" : "old_password_not_match",
            "message" : "old password not match",
        }
    else:
        response_data = {
            "status": "nouser"
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


# post and view in one view
def view_address(request):
    response_data = {}
    redirect_page = request.GET.get('redirect_to')

    if request.user.is_authenticated and not request.user.is_superuser:

        address_instance = CustomerAddress.objects.filter(customer__user=request.user,is_deleted=False)

        if request.method == 'POST':
            # if instance go to edit
            form = AddressForm(request.POST)
            customer = get_user(request.user)


            # print(reverse('web:view_address'),"==========================")
            if form.is_valid():
                data = form.save(commit=False)
                data.auto_id = get_auto_id(CustomerAddress)
                data.creator = request.user
                data.date_updated = datetime.today()
                data.updater = request.user
                data.customer = customer
                data.save()

                form = AddressForm()

                context = {
                    "address_instance": address_instance,

                    'form': form,
                    'page_name' : 'Address',
                    'page_title' : 'Address',
                    'is_need_forms' : True,
                    'is_address' : True,
                }

                if redirect_page == "cart_address":
                    return render(request, 'web/pages/cart-address.html',context)
                else:
                    # print("hai")
                    return render(request, 'web/pages/address-profile.html',context)
                        # print(reverse('web:view_address'),"==========================")

            else:

                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": "Form not currect",
                }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')

        else:
            form = AddressForm()

            context = {
                "address_instance": address_instance,

                'form': form,
                'page_name' : 'Address',
                'page_title' : 'Address',
                'is_need_forms' : True,
                'is_address' : True,
            }

            if redirect_page == "cart_address":
                return render(request, 'web/pages/cart-address.html',context)
            else:
                # print("hai")
                return render(request, 'web/pages/address-profile.html',context)
    else:

        return HttpResponseRedirect(reverse('web:dashboard', ))


def edit_address(request,pk):
    """
    update operation of address
    :param request:
    :param pk:
    :return:
    """
    response_data = {}
    instance = get_object_or_404(CustomerAddress,pk=pk)

    # form = AddressForm(request.POST, instance=instance)
    if request.method == 'POST':
        # if instance go to edit
        form = AddressForm(request.POST, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "successfull",
                "message": "address added successfully completed",
                'redirect': 'true',
                "redirect_url": reverse('web:view_address')

            }

        else:
            # print(form.errors)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": "Form not currect",
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def view_payment(request):
    """
    payment view
    :param request:
    """
    response_data = {}
    if request.user.is_authenticated and not request.user.is_superuser :
        cart_instance = CartItem.objects.filter(customer__user=request.user,is_deleted=False)

        context = {
            'page_title' : 'Payment',
            'page_name' : 'Payment',
            'remove_cod' : cart_instance.filter(product_varient__product__cash_on_delivery=False).exists(),
        }

        return render(request, 'web/pages/payment.html', context)


def my_orders(request):
    if request.user.is_authenticated and not request.user.is_superuser:

        instances = OrderItem.objects.filter(order__customer__user=request.user)

        form = RatingForm(request.POST)

        context = {
            "instances": instances,
            "form" : form,
            'is_my_order' : True,
            'page_name' : 'Orders',
        }

        return render(request, 'web/pages/all-orders.html',context)

    else:

        return HttpResponseRedirect(reverse('web:dashboard', ))


def add_review(request):
    response_data = {}
    if request.user.is_authenticated and not request.user.is_superuser:

        if request.method == 'POST':
            # if instance go to edit
            pro_pk = request.POST['pro_pk']
            instance = get_object_or_404(Product,pk=pro_pk)
            customer = get_user(request.user)
            form = RatingForm(request.POST)

            # if CustomerReview.objects.filter(product__pk=instance.pk,is_deleted=False).exists():


            if form.is_valid():
                data = form.save(commit=False)
                data.auto_id = get_auto_id(CustomerReview)
                data.creator = request.user
                data.date_updated = datetime.today()
                data.updater = request.user

                data.product = instance
                data.customer = customer
                data.save()

                response_data = {
                    "status": "true",
                    "title": "successfull",
                    "message": "Review successfully completed",
                    'redirect': 'true',
                    "redirect_url": reverse('web:my_orders')

                }

            else:
                # print(form.errors)

                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": "Form not currect",
                }

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        return HttpResponseRedirect(reverse('web:dashboard', ))


# single view of order product params using order item pk
def single_view_order(request,pk):
    if request.user.is_authenticated and not request.user.is_superuser:

        instance = OrderItem.objects.get(pk=pk)

        # taking input as the date
        Begindatestring = instance.order.time.date()

        # calculating end date by adding 10 days
        policy_date = Begindatestring + timedelta(days=30)

        form = CancelReasonForm(request.POST)

        context = {
            "instance": instance,
            "form" : form,
            "policy_date" : policy_date,
        }

        return render(request, 'web/pages/single_view_order.html',context)

    else:
        response_data = {
            "status": "nouser"
        }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def cancel_reason(request):
    response_data = {}

    if request.user.is_authenticated and not request.user.is_superuser:

        if request.method == 'POST':
            # if instance go to edit
            order_id = request.POST['order_id']
            pro_id = request.POST['pro_id']

            instance = get_object_or_404(OrderItem,pk=order_id,product_varient__product__pk=pro_id)

            form = CancelReasonForm(request.POST,instance=instance)

            if form.is_valid():
                data = form.save(commit=False)
                data.order_status = "cancelled"
                data.save()

                response_data = {
                    "status": "true",
                    "title": "successfull",
                    "message": "Review successfully completed",
                    'redirect': 'true',
                    "redirect_url": reverse('web:my_orders')
                }

            else:
                # print(form.errors)

                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": "Form not currect",
                }

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        return HttpResponseRedirect(reverse('web:dashboard', ))


def notifications(request):
    if request.user.is_authenticated and not request.user.is_superuser:

        instances = OrderItem.objects.filter(order__customer__user=request.user)

        context = {
            "instances": instances,
            "is_notification" : True,
            'page_name' : 'Notifications',
        }

        return render(request, 'web/pages/notification.html',context)

    else:

        return HttpResponseRedirect(reverse('web:dashboard', ))


# add address pk into temp address table for geting default address for customer
def add_default_address(request):
    address = request.GET.get('address')
    # print(address)
    address_instance = CustomerAddress.objects.get(pk=address)

    response_data = {}

    if request.user.is_authenticated and not request.user.is_superuser:

        customer = get_user(request.user)

        if TempAddress.objects.filter(customer=customer).exists():
            TempAddress.objects.filter(customer=customer).update(address=address_instance)

            # print("if updated")

            response_data = {
                    "status": "true",
                    "title": "successfull",
                    "message": "address added successfully completed",
                    'redirect': 'true',
                    "redirect_url": reverse('web:view_payment')
                }
        else:
            TempAddress.objects.create(
                customer = customer,
                address = address_instance,
            )

            # print("if created")

            response_data = {
                    "status": "true",
                    "title": "successfull",
                    "message": "address added successfully completed",
                    'redirect': 'true',
                    "redirect_url": reverse('web:view_payment')
                }
    else:

        response_data = {
            "status": "nouser"
        }

    # print(response_data)
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def create_order(request):
    payment_type = request.GET.get('payment_type')

    if request.user.is_authenticated and not request.user.is_superuser:
        customer = get_user(request.user)
        cart_instance =  CartItem.objects.filter(customer=customer,is_deleted=False)
        temp_address = TempAddress.objects.get(customer=customer)
        billing_address = CustomerAddress.objects.get(pk=temp_address.address.pk)

        name = billing_address.name
        phone = billing_address.phone
        pincode = billing_address.pincode
        address = billing_address.address
        city = billing_address.city
        state = billing_address.state

        if payment_type == 'payment_by_cod':
            payment_method = 'cash_on_delivery'

        elif payment_type != 'payment_by_cod':
            payment_method = 'online_payment'

        order_auto_id = get_auto_id(Order)
        count_len = len(str(order_auto_id))
        today = datetime.today()
        date_number = ""
        date_count = len(str(today.day))
        if date_count == 1:
            date_number = "0"+str(today.day)
        else :
            date_number = str(today.day)

        month_number = ""
        month_count = len(str(today.month))
        if month_count == 1:
            month_number = "0"+str(today.month)
        else :
            month_number = str(today.month)

        number = ""
        if count_len == 1:
            number = "000" + str(order_auto_id)
        elif count_len == 2:
            number = "00" + str(order_auto_id)
        elif count_len == 3:
            number = "0" + str(order_auto_id)
        else :
            number = str(order_auto_id)

        order_id = "OR" + str(today.year) + month_number + date_number + number

        total_amount = CartItem.objects.filter(customer__user=request.user,is_deleted=False).aggregate(total_price=Sum('unit_price'))["total_price"]
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
            # print(delivery_charge,"charge")

            total_amount = total_amount+delivery_charge
        # print(total_amount,"ttttttttttttttooooooooooooooooooooooooootal")
        order_data = Order.objects.create(
            auto_id = order_auto_id,
            creator = request.user,
            updater = request.user,

            order_id = order_id,
            time = datetime.today(),
            customer = customer,
            billing_name = name,
            billing_phone = phone,
            billing_pincode = pincode,
            billing_address = address,
            billing_city = city,
            billing_state = state,
            total_amount = total_amount,
            payment_method = payment_method,
        )
        #message to customer
        if Location.objects.filter(area=location,is_deleted=False).exists():
            no_of_days =Location.objects.get(area=location,is_deleted=False).min_day_of_delivery
        else:
            no_of_days = 0
        expected_date = order_data.time + timedelta(no_of_days)

        message = f"Dear KIASCO customer, your order {order_data.order_id} is placed and expected delivery by " + str(expected_date.date())
        # msg = sendSMS('placed', order_data.customer.phone, [order_data.order_id, str(expected_date.date())])
        # ('\n\n-------------', msg, '-------------\n\n')

        # print(message)

        for item in cart_instance:
            varient = item.product_varient
            qty = item.qty
            unit_price = item.unit_price

            OrderItem.objects.create(
                auto_id = get_auto_id(OrderItem),
                creator = request.user,
                updater = request.user,

                order = order_data,
                product_varient = varient,
                qty = qty,
                subtotal = unit_price,
            )


            # stock minuse
            # ProductVariant.objects.filter(pk=item.product_varient.pk).update(stock=F("stock")-qty)
        if payment_method != 'online_payment':
            varient.stock-=qty
            varient.save()

            # print("========================")
            # delete item from cart
            # CartItem.objects.filter(pk=item.pk).delete()
            response_data = {
                "status" : "true",
                'redirect' : 'true',
                "redirect_url": reverse("web:cod_success", kwargs={'order_id':order_id})
            }

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            # return HttpResponseRedirect(reverse("web:cod_success", kwargs={'order_id':order_id}))

        if payment_method == 'online_payment':
            Payment.objects.create(
                auto_id = get_auto_id(Payment),
                creator = request.user,
                updater = request.user,

                order_id = order_id,
                currency = "INR",
                description = "New Order",
                payment_mode = "LIVE",
                order_status = "Pending",
                amount = total_amount,
            )
            response_data = {
                "status" : "true",
                "message" : "Online Payment",
                'redirect' : 'true',
                "redirect_url": reverse('web:payment_gateway',kwargs={'order_id':order_id})
            }

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')


        else:
            response_data = {
                "status": "true",
                "title": "successfull",
                "message": "product order successfully completed",
                'redirect': 'true',
                "redirect_url": reverse('web:my_orders')
            }
    else:

        response_data = {
            "status": "nouser"
        }

    # print(response_data)
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@csrf_protect
@csrf_exempt
def payment_gateway(request,order_id):
    if Payment.objects.filter(order_id=order_id,is_deleted=False).exists():
        payment_instance = Payment.objects.get(order_id=order_id,is_deleted=False)
        # print(payment_instance.amount)
        order_instance = Order.objects.get(order_id=order_id,is_deleted=False)
        order_currency = 'INR'
        order_receipt = order_id
        order_amount = payment_instance.amount
        name = order_instance.customer
        email = order_instance.customer.email
        notes = {'Shipping address': order_instance.billing_address}
        total_amount = order_amount * 100


        response = client.order.create(dict(amount=int(float(total_amount)), currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        payment_order_id =response['id']
        Payment.objects.filter(order_id=order_id,is_deleted=False).update(payment_order_id=payment_order_id)

    context = {
        "payment_order_id" : order_instance.order_id,
        "payment_order_id" : payment_order_id,
        "order_amount" : str(order_amount),
        "current_amount" : str(order_amount),
        "name" : name,
        "email" : email,
        "notes" : notes,
        "redirect_url": reverse('web:payment_response', kwargs={'order_id':order_id}),

        'page_name' : 'Payment Page',
        'page_title' : 'Payment Page',

    }

    return render(request, 'web/pages/payment_page.html', context)

#=====================================payment section starting============================#
@csrf_protect
@csrf_exempt
@require_POST
def payment_response(request,order_id):
    # print("payment response")
    response = request.POST

    c = {}
    c.update(csrf(request))

    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }


    payment = Payment.objects.filter(payment_order_id=params_dict['razorpay_order_id'])
    # print(payment,"payment------------")
    order = Order.objects.get(order_id=order_id,is_deleted=False)
    # print(order,"------order----------")
    status = client.utility.verify_payment_signature(params_dict)
    # print(status,"status------------------------")
    if status == False:
        order.payment_status = "failed"
        order.save()

        return render(request, 'web/order_summary.html', {'status': 'Payment Faliure!!!'})
        return HttpResponseRedirect(reverse("web:payment_failed"))


    else:
        # print("else")
        payment.update(
            transaction_id = params_dict['razorpay_payment_id'],
            transaction_signature = params_dict['razorpay_signature'],
            amount = order.total_amount,
            order_status = "ordered",
            payment_datetime = datetime.now(),
        )


        if Customer.objects.filter(user=request.user,is_deleted=False).exists():
            customer = Customer.objects.get(user=request.user,is_deleted=False)
            # print(customer,"---------user------------")
            items = CartItem.objects.filter(customer__user=customer.user,is_deleted=False)
            # print(items,"------------items----------")
        order.payment_status = "received"
        order.save()

        if items:
            # print("inside items")
            for item in items :
                # print(item,"-------------------------ttrttrt")
                product_varient = item.product_varient

                #update stock
                product_varient.stock-=item.qty
                product_varient.save()


                if WhishlistItem.objects.filter(customer = customer,product=product_varient.product).exists():
                    WhishlistItem.objects.filter(customer = customer,product=product_varient.product).delete()

                # item.is_deleted = True
                # item.save()
                # delete item from cart
                CartItem.objects.filter(pk=item.pk,is_deleted=False).delete()

        success = "yes"
        message = "Success! Your transaction has been successfully processed."

        return HttpResponseRedirect(reverse("web:payment_success", kwargs={'order_id':order_id}))


def payments(request):
    title = "Payments"
    instances = Payment.objects.filter(is_deleted=False)
    success = request.GET.get('success')
    message = request.GET.get('message')

    query = request.GET.get("q")
    if query:
        instances = instances.filter(Q(amount__icontains=query) | Q(order_status__icontains=query) | Q(transaction_id__iexact=query) | Q(payment_order_id__iexact=query))
        title = "Payments - %s" %query

    context = {
        "instances" : instances,
        'title' : title,
        "success" : success,
        "message" : message,
        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_grid_system" : True,
        "is_need_animations" : True,
        "is_need_datetime_picker" : True,
    }
    return render(request,'web/pages/payments/payments.html',context)



def payment(request,pk):
    instance = get_object_or_404(Payment.objects.filter(pk=pk,is_deleted=False))
    context = {
        "instance" : instance,
        "title" : "Payment : " + str(instance.amount),
        "single_page" : True,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_grid_system" : True,
        "is_need_animations" : True,
        "is_need_datetime_picker" : True,
    }
    return render(request,'web/pages/payments/payment.html',context)



def payment_success(request,order_id):
    orders =  OrderItem.objects.filter(order__order_id = order_id,is_deleted=False)
    address = Order.objects.get(order_id=order_id,is_deleted=False)

    context = {
        "orders" : orders,
        "address" : address,
        "title" : "Payment Success" ,
    }

    return render(request, 'web/pages/payments/order-successfull.html', context)


def cod_success(request,order_id):
    items = CartItem.objects.filter(customer__user=request.user,is_deleted=False)

    if items:
        # print("inside items")
        for item in items :
            # print(item,"-------------------------ttrttrt")
            product_varient = item.product_varient

            #update stock
            product_varient.stock-=item.qty
            product_varient.save()


            if WhishlistItem.objects.filter(customer__user = request.user,product=product_varient.product).exists():
                WhishlistItem.objects.filter(customer__user = request.user,product=product_varient.product).delete()

            # item.is_deleted = True
            # item.save()
            # delete item from cart
            CartItem.objects.filter(pk=item.pk,is_deleted=False).delete()

    orders =  OrderItem.objects.filter(order__order_id = order_id,is_deleted=False)
    address = Order.objects.get(order_id=order_id,is_deleted=False)

    context = {
        "orders" : orders,
        "address" : address,
        "title" : "Payment Success" ,
    }

    return render(request, 'web/pages/payments/order-successfull.html', context)


def payment_failed(request):

    context = {
        "title" : "Payment Failed",
    }

    return render(request, 'web/pages/payments/failure.html', context)

#===========================================payment section end================================#



def get_products_ajax(request):
    if request.method == "POST":
        filter_id = request.POST['filter_id']
        try:
            instances = Product.objects.filter(category = filter_id)

        except Exception:
            pass


        return JsonResponse(list(instances.values('id', 'title')), safe = False)


def privacy_policy(request):

    context = {

        'page_name' : 'Privacy policy',
        'page_title' : 'Privacy policy',

    }

    return render(request, 'web/pages/privacy.html', context)


def refund_policy(request):

    context = {

        'page_name' : 'Refund policy',
        'page_title' : 'Refund policy',

    }
    return render(request, 'web/pages/refund.html', context)


def shipping_policy(request):


    context = {

        'page_name' : 'Shipping policy',
        'page_title' : 'Shipping policy',

    }
    return render(request, 'web/pages/shipping_policy.html', context)



def terms_of_service(request):


    context = {

        'page_name' : 'Terms of service',
        'page_title' : 'Terms of service',

    }
    return render(request, 'web/pages/terms_of_service.html', context)


def about_us(request):
    description = AboutDescription.objects.filter(is_deleted=False).first()
    gallery = AboutGallery.objects.filter(is_deleted=False)
    customer_reviews = AboutCustomerReview.objects.filter(is_deleted=False)
    context = {
        'description' : description,
        'gallery' : gallery,
        'customer_reviews':customer_reviews,
        'page_name' : 'About us',
        'page_title' : 'About us',

    }
    return render(request, 'web/pages/about_us.html', context)


def invoice(request,pk):

    instance = OrderItem.objects.get(pk=pk)


    context = {
        'instance' : instance,
        'page_name' : 'Invoice',
        'page_title' : 'Invoice',

    }
    return render(request, 'web/pages/invoice.html', context)


from django.contrib.auth.decorators import login_required

from main.decorators import role_required

@login_required
@role_required(['superadmin'])
def about_description(request):
    instance = AboutDescription.objects.first()
    if request.method == "POST":
        form = AboutDescriptionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():

            data = form.save(commit=False)
            data.auto_id = get_auto_id(AboutDescription)
            data.creator = request.user
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "AboutDescription Successfully Updated.",
                "redirect": "true",
                "redirect_url": reverse('web:about_description')
            }
        else:
            message = str(generate_form_errors(form, formset=False))

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = AboutDescriptionForm(instance=instance)
        context = {
            "form": form,
            "title": "AboutDescription Details",
            "instance": instance,
            "redirect": True,
            'page_name' : 'About Description',
            'page_title' : 'About Description',
            'url' : reverse('web:about_description'),
        }

        return render(request, 'admin_panel/general/contacts.html', context)


@login_required
@role_required(['superadmin'])
def about_gallerys(request):
    """
    about_gallery listings
    :param request:
    :return: product list view
    """
    instances = AboutGallery.objects.filter(is_deleted=False)



    context = {
        'instances': instances,
        'page_name' : 'AboutGallerys',
        'page_title' : 'AboutGallerys'
    }

    return render(request, 'admin_panel/web/about_gallerys.html', context)



@login_required
@role_required(['superadmin'])
def create_about_gallery(request):
    """
    create and update operation of about_gallery
    :param request:
    :pk for using edit each about_gallery
    :return:
    """
    if request.method == 'POST':

        form = AboutGalleryForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(AboutGallery)
            data.creator = request.user
            data.date_updated = datetime.now()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "AboutGallery created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:about_gallerys')
            }

        else:
            message = generate_form_errors(form ,formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = AboutGalleryForm()

        context = {
            'form': form,
            'page_name' : 'Create AboutGallery',
            'page_title' : 'Create AboutGallery',
            'is_need_select2' : True,
            'url' : reverse('web:create_about_gallery'),
        }

        return render(request, 'admin_panel/create/create.html',context)



@login_required
@role_required(['superadmin'])
def edit_about_gallery(request,pk):
    """
    edit operation of about_gallery
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(AboutGallery, pk=pk)

    message = ''
    if request.method == 'POST':
        form = AboutGalleryForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.now()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "AboutGallery created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:about_gallerys')
            }

        else:
            message = generate_form_errors(form ,formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = AboutGalleryForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create AboutGallery',
            'page_title' : 'Create AboutGallery',
            'is_need_select2' : True,
            'url' : reverse('web:create_about_gallery'),
        }

        return render(request, 'admin_panel/create/create.html',context)



@login_required
@role_required(['superadmin'])
def delete_about_gallery(request, pk):
    """
    about_gallery deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    AboutGallery.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "AboutGallery Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:about_gallerys')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def about_customer_reviews(request):
    """
    about_customer_review listings
    :param request:
    :return: product list view
    """
    instances = AboutCustomerReview.objects.filter(is_deleted=False)



    context = {
        'instances': instances,
        'page_name' : 'AboutCustomerReviews',
        'page_title' : 'AboutCustomerReviews'
    }

    return render(request, 'admin_panel/web/about_customer_reviews.html', context)



@login_required
@role_required(['superadmin'])
def create_about_customer_review(request):
    """
    create and update operation of about_customer_review
    :param request:
    :pk for using edit each about_customer_review
    :return:
    """
    if request.method == 'POST':

        form = AboutCustomerReviewForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(AboutCustomerReview)
            data.creator = request.user
            data.date_updated = datetime.now()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "AboutCustomerReview created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:about_customer_reviews')
            }

        else:
            message = generate_form_errors(form ,formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = AboutCustomerReviewForm()

        context = {
            'form': form,
            'page_name' : 'Create AboutCustomerReview',
            'page_title' : 'Create AboutCustomerReview',
            'is_need_select2' : True,
            'url' : reverse('web:create_about_customer_review'),
        }

        return render(request, 'admin_panel/create/create.html',context)



@login_required
@role_required(['superadmin'])
def edit_about_customer_review(request,pk):
    """
    edit operation of about_customer_review
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(AboutCustomerReview, pk=pk)

    message = ''
    if request.method == 'POST':
        form = AboutCustomerReviewForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():

            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.now()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "AboutCustomerReview created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:about_customer_reviews')
            }

        else:
            message = generate_form_errors(form ,formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = AboutCustomerReviewForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create AboutCustomerReview',
            'page_title' : 'Create AboutCustomerReview',
            'is_need_select2' : True,
            'url' : reverse('web:create_about_customer_review'),
        }

        return render(request, 'admin_panel/create/create.html',context)



@login_required
@role_required(['superadmin'])
def delete_about_customer_review(request, pk):
    """
    about_customer_review deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    AboutCustomerReview.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "AboutCustomerReview Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:about_customer_reviews')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

