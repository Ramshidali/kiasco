from . import views
from django.urls import path, re_path

app_name = 'general'

urlpatterns = [
    path('locations/', views.locations, name='locations'),
    re_path(r'^create-location/$', views.create_location, name='create_location'),
    re_path(r'^edit-location/(?P<pk>.*)/$', views.edit_location, name='edit_location'),
    re_path(r'^delete-location/(?P<pk>.*)/$', views.delete_location, name='delete_location'),

    path('banners/', views.banners, name='banners'),
    re_path(r'^create-banner/$', views.create_banner, name='create_banner'),
    re_path(r'^delete-banner/(?P<pk>.*)/$', views.delete_banner, name='delete_banner'),
    re_path(r'^update-contacts/$', views.update_contacts, name='update_contacts'),
    
    re_path(r'^upload-locations/$', views.upload_locations, name='upload_locations'),
]