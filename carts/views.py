from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Cart,CartItem
from orders.models import Order
from products.models import Product
from accounts.forms import LoginForm, GuestForm
from billings.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from analytics.signals import object_viewed_signal
from billings.models import Charge

from category.models import Category

import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_7R9QtO5N29ROUi0rSpUYv7N700ZwN4w3mf")
STRIPE_PUB_KEY = getattr(settings, STRIPE_SECRET_KEY, "pk_test_O6wiMgMeQ0vOb6q24zKjRCoK00ATArkfbL")
stripe.api_key = STRIPE_SECRET_KEY


# Cart Home section
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    
    cart_items = cart_obj.cartitem_set.all()
    subtotal = 0
    notes = []
    for item in cart_items:
        notes += [item.notes]
        subtotal += (item.product.price * item.quantity)
    cart_obj.subtotal = subtotal 
    cart_obj.save()
    if cart_obj.subtotal >= 0:
        cart_obj.total = cart_obj.subtotal 
        cart_obj.save()            
    
    request.session['cart_total'] = cart_obj.cartitem_set.all().count()
    category_qs = Category.objects.filter(active=True)
    # object_viewed_signal.send(cart_obj.__class__, instance=cart_obj, request=request)
    context = {
        'cart_obj':cart_obj, 
        'category_qs': category_qs
    }
    return render(request, 'carts/home.html', context)

# Add to cart and cart Remove section
def cart_update(request):
    product_id = request.GET.get('product_id')
    try:
        product_obj = Product.objects.get(id=product_id)
    except:
        return redirect('carts:home')
    # quantity 
    try:
        qty = request.GET.get('qty')
        update_qty = True 
    except: 
        qty = None 
        update_qty = False
        
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    try:
        cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        if cart_item or created:
            added = True 
    except Exception as e: 
        print(e)
    
    if update_qty and qty:
        if int(qty) == 0:
            cart_item.delete()
            added=False
        else:
            cart_item.quantity = qty 
            cart_item.save()
    else:
        pass
    request.session['cart_total'] = cart_obj.cartitem_set.all().count()
    cartCount = cart_obj.cartitem_set.all().count()
    if request.is_ajax():
        json_data = {
            "added": added,
            "remove": not added,
            "cartCount": cartCount
        }
        return JsonResponse(json_data)
    return redirect("carts:home")



from analytics.mixins import ObjectViewedMixin

# Checkout section
def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.cartitem_set.all().count() == 0:
        return redirect('carts:home')
    
    login_form = LoginForm()
    guest_form = GuestForm()
    shipping_address_form = AddressForm()
    # billing_address_form = AddressForm()
        
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    shipping_address_id = request.session.get("shipping_address_id", None)
    # billing_address_id = request.session.get("billing_address_id", None)
    
    address_qs = None
    shipping_address_qs = None
    # billing_address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            shipping_address_qs = address_qs.filter(billing_profile=billing_profile)
            # billing_address_qs = address_qs.filter(address_type='billing')
        
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        # if billing_address_id:
        #     order_obj.billing_address = Address.objects.get(id=billing_address_id)
        #     del request.session["billing_address_id"]
        if shipping_address_id: # or billing_address_id
            order_obj.save()
            
        has_card = billing_profile.has_card
    
    # checkout finalize and payment method
    if request.method == 'POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, charge_msg = billing_profile.charge(order_obj) # Charge.objects.do(billing_profile, order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_total'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("/carts/success")
            else:
                print(charge_msg)
                return redirect("carts:checkout")
            
    category_qs = Category.objects.filter(active=True)
    context = {
        "billing_profile": billing_profile,
        "object": order_obj,
        "login_form": login_form,
        "guest_form": guest_form,
        "shipping_address_form":shipping_address_form,
        # "billing_address_form": billing_address_form,
        "shipping_address_qs": shipping_address_qs,
        # "billing_address_qs": billing_address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
        "category_qs": category_qs
    }
    return render(request, "carts/checkout.html", context)



def checkout_done(request):
    category_qs = Category.objects.filter(active=True)
    context = {
        "category_qs": category_qs
    }
    return render(request, "carts/checkout_done.html", context)


