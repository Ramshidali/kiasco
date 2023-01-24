from django.contrib import admin
from django.views.static import serve
from django.urls import include, path, re_path
from kiasco import settings
from main import views as general_views

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('kiasco-admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    path('kiasco-super-admin/',include(('main.urls'),namespace='main')),   
    path('kiasco-super-admin/',general_views.app,name='app'), 
    
    # admin panel
    path('kiasco-super-admin/product/',include(('product.urls'),namespace='product')),
    path('kiasco-super-admin/customers/',include(('customers.urls'),namespace='customers')),
    path('kiasco-super-admin/orders/',include(('orders.urls'),namespace='orders')),
    path('kiasco-super-admin/general/',include(('general.urls'),namespace='general')),
    path('kiasco-super-admin/offers/',include(('offers.urls'),namespace='offers')),
    path('kiasco-super-admin/payments/',include(('payments.urls'),namespace='payments')),
    path('kiasco-super-admin/reports/',include(('reports.urls'),namespace='reports')),
    
    # web
    path('',include(('web.urls'),namespace='web')),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
