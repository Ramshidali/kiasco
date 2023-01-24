from django.urls import path, re_path
from . import views

app_name = 'orders'

urlpatterns = [
    re_path(r'^orders/$', views.orders, name='orders'),
    re_path(r'^order-item/(?P<pk>.*)/$', views.order_item, name='order_item'),
    re_path(r'^change-order-status/(?P<pk>.*)/$', views.change_order_status, name='change_order_status'),
    re_path(r'^add-tracking-details/(?P<pk>.*)/$', views.add_tracking_details, name='add_tracking_details'),
]