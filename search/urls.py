from django.urls import path  

from .views import SearchingProductList 

app_name = 'search'

urlpatterns = [
    path('', SearchingProductList.as_view(), name='search')
]

