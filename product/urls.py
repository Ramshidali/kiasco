from django.urls import path, re_path
from . import views
from product.views import CategoryAutocomplete

app_name = 'product'

urlpatterns = [
    re_path(r'^delivery-locations-autocomplete/$', views.DeliveryLocationsAutocomplete.as_view(),
            name='delivery_locations_autocomplete'),
    re_path(r'^meta-keywords-autocomplete/$', views.MetaKeywordsAutocomplete.as_view(),
            name='meta_keywords_autocomplete'),
    path('category-autocomplete/', CategoryAutocomplete.as_view(create_field='name'),name='category_autocomplete'),
    
    path('meta-keyword/', views.meta_keyword, name='meta_keyword'),
    re_path(r'^create-meta-keyword/$', views.create_meta_keyword, name='create_meta_keyword'),
    re_path(r'^edit-meta-keyword/(?P<pk>.*)/$', views.edit_meta_keyword, name='edit_meta_keyword'),
    re_path(r'^delete-meta-keyword/(?P<pk>.*)/$', views.delete_meta_keyword, name='delete_meta_keyword'),
    
    path('product-list/', views.product_list, name='product_list'),
    re_path(r'^product-details/(?P<pk>.*)/$', views.product_details, name='product_details'),
    re_path(r'^create-product/$', views.create_product, name='create_product'),
    re_path(r'^edit-product/(?P<pk>.*)/$', views.edit_product, name='edit_product'),
    re_path(r'^delete-product/(?P<pk>.*)/$', views.delete_product, name='delete_product'),
    re_path(r'^delete-product-variant/(?P<pk>.*)/$', views.delete_product_varient, name='delete_product_varient'),
    
    path('product-size-chart/', views.size_chart, name='size_chart'),
    re_path(r'^check-product-type/$', views.check_product_type, name='check_product_type'),
    re_path(r'^create-size-chart/$', views.create_size_chart, name='create_size_chart'),
    re_path(r'^edit-size-chart/(?P<pk>.*)/$', views.edit_sizechart, name='edit_sizechart'),
    re_path(r'^delete-size/(?P<pk>.*)/$', views.delete_size, name='delete_size'),
    re_path(r'^delete-category-size/(?P<c_pk>.*)/$', views.delete_size_category, name='delete_size_category'),     
    
   
    re_path(r'^edit-size-image-chart/(?P<pk>.*)/$', views.edit_sizechart_image, name='edit_sizechart_image'),
    re_path(r'^delete-image-size/(?P<pk>.*)/$', views.delete_size_image, name='delete_size_image'),
   
	re_path(r'^update-locations/(?P<pk>.*)/$',views.update_locations, name='update_locations'),
   
    path('product-category/', views.product_category, name='product_category'),
    re_path(r'^create-product-category/$', views.create_product_category, name='create_product_category'),
    re_path(r'^edit-product-category/(?P<pk>.*)/$', views.edit_product_category, name='edit_product_category'),
    re_path(r'^delete-product-category/(?P<pk>.*)/$', views.delete_product_category, name='delete_product_category'),
    
#     path('product-type/', views.product_type, name='product_type'),
#     re_path(r'^create-product-type/$', views.create_product_type, name='create_product_type'),
#     re_path(r'^edit-product-type/(?P<pk>.*)/$', views.edit_product_type, name='edit_product_type'),
#     re_path(r'^delete-product-type/(?P<pk>.*)/$', views.delete_product_type, name='delete_product_type'),
]
