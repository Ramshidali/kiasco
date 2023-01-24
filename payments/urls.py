from django.urls import path, re_path
from . import views


app_name = 'payments'

urlpatterns = [
    re_path(r'^payments/$', views.payments, name='payments'),
    re_path(r'^payment/(?P<pk>.*)/$', views.payment, name='payment'),
]
