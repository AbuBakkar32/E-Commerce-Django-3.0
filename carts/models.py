from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models import Product  

User = get_user_model()

class CartManager(models.Manager):
    def new_or_get(self, request):
        # request.session.set_expiry(180)
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id, active=True)
        
        cart_qs = None
        if request.user.is_authenticated:
            cart_qs = Cart.objects.filter(user=request.user, active=True)
            if cart_qs.exists():
                cart_obj = cart_qs.first()
                new_obj = False
            else:
                cart_obj = Cart.objects.create(user=request.user)
                request.session['cart_id'] = cart_obj.id
                new_obj = True
                
            qs = self.get_queryset().filter(id=cart_id, active=True, user=None)
            cart_items = None
            if qs.count() == 1:
                qs_obj = qs.first()
                cart_items = qs_obj.cartitem_set.all()
                if cart_items is not None:
                    products = []
                    for item in cart_obj.cartitem_set.all():
                        products += [item.product]
                    for cart_item in cart_items:
                        if cart_item.product not in products:
                            cart_item.cart = cart_obj 
                            cart_item.save()
                                    
                qs.update(active=False) 
        else:
            if qs.count() == 1:
                new_obj = False
                cart_obj = qs.first()
            else:
                cart_obj = Cart.objects.create(user=None)
                new_obj = True
                request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
    
class CartItem(models.Model):
    cart        = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True, blank=True)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity    = models.PositiveIntegerField(default=1)
    notes       = models.TextField(null=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product}-->{self.quantity}"
    
class Cart(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # product         = models.ManyToManyField(Product, blank=True)
    subtotal        = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total           = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active          = models.BooleanField(default=True)
    update          = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


# def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = instance.product.all()
#         subtotal = 0
#         for x in products:
#             subtotal += x.price
#         if instance.subtotal != subtotal:
#             instance.subtotal = subtotal
#             instance.save()

# m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.product.through)


# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     if instance.subtotal > 0:
#         instance.total = instance.subtotal + 5
#     else:
#         instance.total = 0.00

# pre_save.connect(pre_save_cart_receiver, sender=Cart)







