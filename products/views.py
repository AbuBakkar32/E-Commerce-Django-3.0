from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model

from .models import Product

from carts.models import Cart,CartItem

# from analytics.signals import object_viewed_signal

# from analytics.mixins import ObjectViewedMixin

from category.models import Category

User = get_user_model()
# product-list
class ProductList(ListView):
    model = Product  
    template_name = 'products/product-list.html'
    context_object_name = 'query'
    # ordering = ['price']

    def get_context_data(self, *args, **kwargs):
        context = super(ProductList, self).get_context_data(*args, **kwargs)
        context['category_qs'] = Category.objects.filter(active=True)
        return context


# product-detail
class ProductDetail(DetailView):
    model = Product  
    template_name = 'products/product-detail.html'
    # context_object_name = 'object'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetail, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        product_slug = self.kwargs['slug']
        product_obj = Product.objects.get(slug=product_slug)
        
        context['user'] = User.objects.all()
        context['cart'] = cart_obj
        try:
            cart_item1 = CartItem.objects.get(cart=cart_obj, product=product_obj)
        except:
            cart_item1 = None
        context['cart_item'] = cart_item1
        
        context['category_qs'] = Category.objects.filter(active=True)
        return context  

    def get_object(self, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Not Found!")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance 




# product detail FUNCTION BASED

# def product_detail(request, pk, *args, **kwargs):
#     # pk = kwargs['pk']
#     # instance = Product.objects.get(pk=pk)

#     instance = get_object_or_404(Product, pk=pk)
#     # lis = Product.objects.all()
#     context = {
#         # 'objects': lis,
#         'object': instance
#         # 'hi': 'Hello'
#     }
#     return render(request, 'products/product-detail.html', context)


# product LIST FUNCTION BASED

# def product_list(request):
#     query = Product.objects.all()
#     context = {
#         'query': query
#     }
#     return render(request, 'products/product-list.html', context)



