from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from category.models import Category
from .models import BillingProfile, Card

import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_7R9QtO5N29ROUi0rSpUYv7N700ZwN4w3mf")
STRIPE_PUB_KEY = getattr(settings, STRIPE_SECRET_KEY, "pk_test_O6wiMgMeQ0vOb6q24zKjRCoK00ATArkfbL")
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    qs = Category.objects.filter(active=True)
    if not billing_profile:
        return redirect("/carts")
    
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billings/payment-method.html', {'publish_key': STRIPE_PUB_KEY, 'next_url': next_url, 'category_qs': qs })


def payment_method_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({'message': "Cann't find this user."}, status=401)
        
        token = request.POST.get('token')
        if token is not None:           
            Card.objects.add_new(billing_profile, token)
        
        return JsonResponse({'message': 'Success! your card was added.'})
    return HttpResponse('error', status=401)