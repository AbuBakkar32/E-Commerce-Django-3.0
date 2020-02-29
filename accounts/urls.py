from django.urls import path  
from django.contrib.auth.views import LoginView, LogoutView

from .views import  (UserLoginView, 
                    guest_user_register, 
                    user_logout,
                    RegistrationVeiw,
                    user_profile_view,
                    EmailActivationView,
                    order_list_view,
                    order_detail_view,
                    account_settings)


app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    # path('logout/', LogoutView.as_view(template_name='accounts/auth/logout.html'), name='logout'),
    path('register/', RegistrationVeiw.as_view(), name='register'),
    path('register/guest/', guest_user_register, name='guest-register'),

    path('profile_detail/', user_profile_view, name='profile_detail'),
    path('profile_settings/', account_settings, name='account_settings'),
    path('order_list/', order_list_view, name='order-list'),
    path('order_detail/<order_id>/', order_detail_view, name='order-detail'),

    path('confirm/<key>/', EmailActivationView.as_view(), name='email-activation'),
    
]


