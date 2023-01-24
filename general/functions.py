import string
import random
from django.http import HttpResponse
from decimal import Decimal
import datetime
from django.conf import settings
import requests
from django.db.models import Max
from general.models import Location


def get_otp(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_string(size=6, chars=string.ascii_lowercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    return ipaddress


def get_auto_id(model):
    auto_id = 1
    latest_auto_id = model.objects.aggregate(Max('auto_id'))
    max_auto_id = latest_auto_id['auto_id__max']
    if max_auto_id:
        auto_id = int(max_auto_id) + 1

    return auto_id


def generate_form_errors(args, formset=False):
    i = 1
    message = ""
    if not formset:
        for field in args:
            if field.errors:
                message += "\n"
                message += field.label + " : "
                message += str(field.errors)

        for err in args.non_field_errors():
            message += str(err)
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += "\n"
                    message += field.label + " : "
                    message += str(field.errors)
            for err in form.non_field_errors():
                message += str(err)

    message = message.replace("<li>", "")
    message = message.replace("</li>", "")
    message = message.replace('<ul class="errorlist">', "")
    message = message.replace("</ul>", "")
    return message


def get_a_id(model, request):
    a_id = 1
    latest_a_id = model.objects.all().order_by("-date_added")[:1]
    if latest_a_id:
        for auto in latest_a_id:
            a_id = auto.a_id + 1
    return a_id


def get_current_role(request):
    is_superadmin = False
    is_administrator = False
    is_customer = False
    is_vendor = False
    is_delivery_agent = False

    current_role = "user"
    if request.user.is_authenticated:
        groups = request.user.groups.all()

        if request.user.is_superuser:
            is_superadmin = True
        elif groups.filter(name="administrator").exists():
            is_administrator = True
        elif groups.filter(name="customer").exists():
            is_customer = True
        elif groups.filter(name="vendor").exists():
            is_vendor = True
        elif groups.filter(name="delivery_agent").exists():
            is_delivery_agent = True

        if "current_role" in request.session:
            role = request.session['current_role']
            if role == "superadmin":
                current_role = "superadmin"
            elif role == "vendor":
                current_role = "vendor"
            elif role == "delivery_agent":
                current_role = "delivery_agent"
            elif role == "customer":
                current_role = "customer"
            elif role == "administrator":
                current_role = "administrator"
        else:
            if is_superadmin:
                current_role = "superadmin"
            elif is_customer:
                current_role = "customer"
            elif is_vendor:
                current_role = "vendor"
            elif is_administrator:
                current_role = "administrator"
            elif is_delivery_agent:
                current_role = "delivery_agent"

        return current_role


def get_placeholder():
    image = 'https://i2.wp.com/quidtree.com/wp-content/uploads/2020/01/placeholder.png?fit=1200%2C800&ssl=1'
    return image


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


