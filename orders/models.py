from django.db import models
from django.db.models.signals import pre_save, post_save

from carts.models import Cart
from billings.models import BillingProfile
from ecommerce.utils import unique_order_id_generator
from django.core.signals import request_finished
from django.dispatch import receiver
from addresses.models import Address


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, 
                                        cart=cart_obj, 
                                        active=True,
                                        status="created")
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created=True
        return obj, created


class Order(models.Model):
    order_id            = models.CharField(max_length=120, blank=True)
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address    = models.ForeignKey(Address, related_name="shipping_address", on_delete=models.CASCADE, null=True, blank=True)
    # billing_address     = models.ForeignKey(Address, related_name="billing_address", on_delete=models.CASCADE, null=True, blank=True)
    cart                = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ORDER_STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancel', 'Cancel')
        # ('refunded', 'Refunded')
    )
    PAYMENT_OPTION = (
        ('cash_on_delivery', 'Cash On Delivery'),
        ('bkash', 'Bkash'),
        ('card', 'Card'),
        ('rocket', 'Rocket')
    )
    status              = models.CharField(max_length=15, default='created', choices=ORDER_STATUS_CHOICES)
    payment_by          = models.CharField(max_length=20, choices=PAYMENT_OPTION, default='card')
    shipping_total      = models.DecimalField(max_digits=20, default=40, decimal_places=2)
    total               = models.DecimalField(max_digits=120, default=0.00, decimal_places=2)
    active              = models.BooleanField(default=True)
    is_shipped          = models.BooleanField(default=False)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    

    objects = OrderManager()

    class Meta:
        ordering=["-timestamp"]



    def __str__(self):
        return self.order_id

    def update_total(self):
        shipping_total = self.shipping_total
        cart_total = self.cart.total 
        new_total = float(shipping_total) + float(cart_total)
        new_total = "%.2f"%(new_total)
        self.total = new_total 
        self.save()
        return new_total 
    
    def check_done(self):
        billing_profile = self.billing_profile
        # billing_address = self.billing_address
        shipping_address = self.shipping_address
        total = self.total 
        
        if billing_profile and shipping_address and total > 0:
            return True
        return False
    
    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.cart.active = False
            self.cart.save()
            self.save()
        return self.status


# Get order id
def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    qs = Order.objects.exclude(billing_profile=instance.billing_profile).filter(cart=instance.cart, active=True)
    if qs.exists():
        qs.update(active=False)
pre_save.connect(pre_save_order_id_receiver, sender = Order)


# Update order total from cart
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_id = instance.id 
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
post_save.connect(post_save_cart_total, sender=Cart)

# Update order total from order
def post_save_order(sender, instance,  created, *args, **kwargs):
    if created:
        instance.update_total()
        if instance.is_shipped:
            print(instance.status)
post_save.connect(post_save_order, sender=Order)


    
