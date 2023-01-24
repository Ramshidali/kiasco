from django.urls import path, re_path
from . import views

app_name = 'offers'

urlpatterns = [
    path('offers/', views.offers, name='offers'),
    re_path(r'^create-offer/(?P<pk>.*)/$', views.create_offer, name='create_offer'),
    # re_path(r'^edit-meta-keyword/(?P<pk>.*)/$', views.edit_meta_keyword, name='edit_meta_keyword'),
    re_path(r'^delete-offer/(?P<pk>.*)/$', views.delete_offer, name='delete_offer'),
]