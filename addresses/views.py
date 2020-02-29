from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from addresses.forms import AddressForm
from billings.models import BillingProfile
from .models import Address



def checkout_address_create_view(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            # address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            # instance.address_type = address_type
            instance.save()
            
            request.session["shipping_address_id"] = instance.id
            
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('carts:checkout')
    return redirect("carts:checkout")


def checkout_address_reuse_view(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    
    if request.method == 'POST':
        address_id = request.POST.get('address', None)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        # address_type = request.POST.get('address_type', 'shipping')
        if address_id is not None:
            if request.user.is_authenticated:
                qs = Address.objects.filter(billing_profile=billing_profile, id=address_id)
                if qs.exists():  
                    request.session["shipping_address_id"] = address_id
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("carts:checkout")
        
    
