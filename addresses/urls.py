from django.urls import path  

from .views import checkout_address_create_view, checkout_address_reuse_view

app_name='addresses'

urlpatterns = [
    path('create/', checkout_address_create_view, name='checkout_address_create'),
    path('create/reuse/', checkout_address_reuse_view, name='checkout_address_reuse')
]


