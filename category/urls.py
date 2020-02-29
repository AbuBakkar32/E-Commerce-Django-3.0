from django.urls import path  

from .views import category_list, category_detail, sub_category_detail

app_name = "category"

urlpatterns = [
    path('lists/', category_list, name='list'),
    path('detail/<int:pk>/', category_detail, name='detail'),
    path('sub-category/detail/<int:pk>/', sub_category_detail, name='sub-detail')
]



