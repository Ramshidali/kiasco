from django.urls import path, re_path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),

    #*******************************************sign up section********************************#

    re_path(r'^otp-generation/$', views.otp_generation, name='otp_generation'),
    re_path(r'^otp-verification/$', views.verify_otp, name='verify_otp'),

    re_path(r'^customer-join/$', views.customer_join, name='customer_join'),
    re_path(r'^signup/$', views.signup, name='signup'),
    
    re_path(r'^verify-email-otp/$', views.verify_email_otp, name='verify_email_otp'),
    
    path('logout/', views.customer_logout, name='logout'),
    
    # re_path(r'^email-otp-generation/$', views.email_otp_generation, name='email_otp_generation'),

    # re_path(r'^customer-signup/$', views.customer_signup, name='customer_signup'),
    # re_path(r'^customer-signin/$', views.customer_signin, name='customer_signin'),

    # re_path(r'^check-user/$', views.check_user, name='check_user'),
    # re_path(r'^forgot-password/$', views.forgot_password, name='forgot_password'),

    #*******************************************products********************************#

    path('shop/', views.shop, name='shop'),
    path('new-collection/', views.new_collection, name='new_collection'),

    re_path(r'^product-view/(?P<pk>.*)/$', views.product_view, name='product_view'),
    re_path(r'^show-all-product/(?P<pk>.*)/$', views.show_all_product, name='show_all_product'),
    re_path(r'^check-varient/$', views.check_varient, name='check_varient'),

    re_path(r'^add-to-wishlist/$', views.add_to_wishlist, name='add_to_wishlist'),
    re_path(r'^view-wishlist/$', views.view_wishlist, name='view_wishlist'),

    re_path(r'^view-cart/$', views.view_cart, name='view_cart'), #
    re_path(r'^add-to-cart/$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^remove-from-cart/$', views.remove_from_cart, name='remove_from_cart'),
    re_path(r'^increment-cart/$', views.increment_cart, name='increment_cart'),
    re_path(r'^decrement-cart/$', views.decrement_cart, name='decrement_cart'),

    re_path(r'^check-pincode/$', views.check_pincode, name='check_pincode'),

    path('profile/', views.profile, name='profile'),
    re_path(r'^change-profile-details/$', views.change_profile_details, name='change_profile_details'),
    re_path(r'^change-password/$', views.change_password, name='change_password'),

    re_path(r'^generate-phone-otp/$', views.generate_phone_otp, name='generate_phone_otp'),
    re_path(r'^change-phone/$', views.change_phone_number, name='change_phone_number'),

    path('my-orders/', views.my_orders, name='my_orders'),
    re_path(r'^single-view-order/(?P<pk>.*)/$', views.single_view_order, name='single_view_order'),
    re_path(r'^add-review/$', views.add_review, name='add_review'),
    re_path(r'^cancel-reason/$', views.cancel_reason, name='cancel_reason'),

    path('notifications/', views.notifications, name='notifications'),

    path('view-address/', views.view_address, name='view_address'),
    re_path(r'^add-default-address/$', views.add_default_address, name='add_default_address'),
    re_path(r'^edit-address/(?P<pk>.*)/$', views.edit_address, name='edit_address'),

    path('view-payment/', views.view_payment, name='view_payment'),
    re_path(r'^create-order/$', views.create_order, name='create_order'),
    re_path(r'^payment-gateway/(?P<order_id>.*)/$', views.payment_gateway, name='payment_gateway'),

    re_path(r'^payment-response/(?P<order_id>.*)/$', views.payment_response, name="payment_response"),
    re_path(r'^payments/$',views.payments,name='payments'),
    re_path(r'^payment/(?P<pk>.*)/$',views.payment,name='payment'),
    re_path(r'^payment-success/(?P<order_id>.*)/$', views.payment_success, name="payment_success"),
    re_path(r'^cod-success/(?P<order_id>.*)/$', views.cod_success, name="cod_success"),
    re_path(r'^payment-failed/$', views.payment_failed, name="payment_failed"),


    path('get-products-ajax/', views.get_products_ajax, name="get_products_ajax"),

    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),

    path('about-us/', views.about_us, name='about_us'),
    re_path(r'^invoice/(?P<pk>.*)/$', views.invoice, name='invoice'),

    re_path(r'^about-description/$', views.about_description, name='about_description'),

    re_path(r'^about_gallerys/', views.about_gallerys, name='about_gallerys'),
    re_path(r'^create-about_gallery/$', views.create_about_gallery, name='create_about_gallery'),
    re_path(r'^edit-about_gallery/(?P<pk>.*)/$', views.edit_about_gallery, name='edit_about_gallery'),
    re_path(r'^delete-about_gallery/(?P<pk>.*)/$', views.delete_about_gallery, name='delete_about_gallery'),

    re_path(r'^about_customer_reviews/', views.about_customer_reviews, name='about_customer_reviews'),
    re_path(r'^create-about_customer_review/$', views.create_about_customer_review, name='create_about_customer_review'),
    re_path(r'^edit-about_customer_review/(?P<pk>.*)/$', views.edit_about_customer_review, name='edit_about_customer_review'),
    re_path(r'^delete-about_customer_review/(?P<pk>.*)/$', views.delete_about_customer_review, name='delete_about_customer_review'),

]