#Standard
import string
import random
import random
import string
import requests
from cryptography.fernet import Fernet
#Django
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
#Third Party
from mailqueue.models import MailerMessage
from random import randint
#Local
from customers.models import Customer


def generate_unique_id(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_form_errors(args,formset=False):
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
    

def get_auto_id(model):
    auto_id = 1
    try:
        latest_auto_id =  model.objects.all().order_by("-date_added")[:1]
        if latest_auto_id:
            for auto in latest_auto_id:
                auto_id = auto.auto_id + 1
    except:
        pass
    return auto_id


def get_current_role(request):
    is_superadmin = False
    is_staff = False
    is_dealer = False

    if request.user.is_authenticated:        
        
        if User.objects.filter(id=request.user.id,is_superuser=True,is_active=True).exists():
            is_superadmin = True
        
        if User.objects.filter(id=request.user.id,is_active=True,groups__name="staff").exists():
            is_staff = True

    current_role = "user"
    if is_superadmin:
        current_role = "superadmin"
    elif is_staff:
        current_role = "staff"
                
    return current_role


def randomnumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def paginate(instances, request):
    paginator = Paginator(instances, 20)
    page_number = request.GET.get('page')
    instances = paginator.get_page(page_number)

    return instances

def get_otp(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def load_key():
    key = getattr(settings, "PASSWORD_ENCRYPTION_KEY", None)
    if key:
        return key
    else:
        raise ImproperlyConfigured("No configuration  found in your PASSWORD_ENCRYPTION_KEY setting.")

def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return(encrypted_message.decode("utf-8"))

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()

def get_user(user):
    user = Customer.objects.get(user=user)
    return user


def sendSMS(message_type, numbers, variables_values=[]):
    key = 'Zhi2AyfdE7GVHLj9Re6CgqFD1MtslBQnXczPxow48JNO0Kabp3JPiIwqX0feSmgREuZCHMbd5o9kUn6G'
    values = '|'.join(variables_values)
    is_ok = True

    if message_type == 'otp':
        message_id = 140147
        # variables = otp

    elif message_type == 'placed':
        message_id = 140148
        # variables = order_id, date

    elif message_type == 'shipped':
        message_id = 140150
        # variables = order_id, tracking_id, expected_time

    elif message_type == 'delivered':
        message_id = 140152
        # variables = date

    elif message_type == 'cancelled':
        message_id = 140149
        # variables = order_id

    else:
        is_ok = False

    if is_ok:
        url = f"https://www.fast2sms.com/dev/bulkV2?authorization={key}&route=dlt&sender_id=KIASCO&message={message_id}&variables_values={values}&flash=0&numbers={numbers}"
        r = requests.get(url=url)
        data = r.content

        return data
    else:
        return ''
    
    
def send_email(subject,to_address,content,bcc_address=settings.DEFAULT_BCC_EMAIL,app="kiasco",reply_to_address=settings.DEFAULT_REPLY_TO_EMAIL,attachment=None):
    print("send fun")
    new_message = MailerMessage()
    new_message.subject = subject
    new_message.to_address = to_address
    if bcc_address:
        new_message.bcc_address = bcc_address
    new_message.from_address = settings.DEFAULT_FROM_EMAIL
    new_message.content = content
    # new_message.html_content = html_content
    new_message.app = app
    if attachment:
        new_message.add_attachment(attachment)
    new_message.reply_to = reply_to_address
    new_message.save()