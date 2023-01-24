from customers.models import Customer

def get_user(user):
    user = Customer.objects.get(phone=user)
    return user

