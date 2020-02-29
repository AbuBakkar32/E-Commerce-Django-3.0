from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from products.models import Product 

from category.models import Category 


class SearchingProductList(ListView):
    model = Product  
    template_name = 'products/product-list.html'
    context_object_name = 'query'
    # ordering = ['price']

    def get_queryset(self):
        qs = Product.objects.all()
        
        # department filter
        query = self.request.GET.get('c_base_q' or None)
        if query is not None:
            qs = Product.objects.filter(
                Q(department_name__name__iexact=query)
            )
            
        # input filter 
        query2 = self.request.GET.get('q' or None)
        if query2 is not None:
            qs = qs.filter(
                Q(title__icontains=query2)| 
                Q(tag__title__icontains=query2)
            ).distinct()
        return qs
    
    def get_context_data(self, *args, **kwargs):
        context = super(SearchingProductList, self).get_context_data(*args, **kwargs)
        context['category_qs'] = Category.objects.filter(active=True)
        return context
    
    
    