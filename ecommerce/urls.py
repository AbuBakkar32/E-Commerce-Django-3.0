"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static 

from django.contrib import admin
from django.urls import path, include


from .views import (home_page, 
                    about_page, 
                    contact_page,
                    privacy_policy)

from billings.views import payment_method_view, payment_method_create_view      

urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('privacy/policy/', privacy_policy, name='privacy_policy'),
    
    path('billings/payment-method/', payment_method_view, name='payment-method'),
    path('billings/payment-method/create/', payment_method_create_view, name='payment-method-endpoint'),

    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('search/', include('search.urls')),
    path('carts/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('address/', include('addresses.urls')),
    path('category/', include('category.urls')),

    path('accounts/', include('accounts.passwords.urls')),
    # path('billings/', include('billings.urls'))
]

if settings.DEBUG:
    urlpatterns += \
            static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += \
            static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)