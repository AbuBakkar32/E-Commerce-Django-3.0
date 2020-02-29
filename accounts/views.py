from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
# from .signals import user_login_signal
from .models import GuestEmail, EmailActivation
from .forms import RegistrationForm, LoginForm, GuestForm, UserProfileForm, UserEdit, UserProfileEdit
from django.db.models import Q
from category.models import Category
from orders.models import Order
from billings.models import BillingProfile
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from .models import UserProfile

User = get_user_model()


class EmailActivationView(View):
    def get(self, request, key, *args, **kwargs):
        qs = EmailActivation.objects.filter(key__iexact=key)
        confirm_qs = qs.confirmable()
        if confirm_qs.count() == 1:
            obj=confirm_qs.first()
            obj.activate()
            messages.success(request, "Your email has been confirmed, now you can login!")
            return redirect("accounts:login")
        else:
            activated_qs = qs.filter(activated=True)
            if activated_qs.exists():
                reset_link = reverse('password_reset')
                msg = """Your email has already been confirmed,
                        Do you need to <a href="{reset_link}">reset your password?</a>
                """.format(reset_link=reset_link)
                messages.success(request, mark_safe(msg))
                return redirect("accounts:login")

        return render(request, "registration/activation-error.html", {})



# User Registration section
class RegistrationVeiw(SuccessMessageMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login'
    success_message = "We sent an email to your accout with some instruction.Please check it and active account."

    
    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationVeiw, self).get_context_data(*args, **kwargs)
        context['category_qs']=Category.objects.filter(active=True)
        return context 
    


# def user_register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data['password1'])
#             print(form.cleaned_data['password2'])
#             messages.success(request, 'Registration complete...now you can login...')
#             return redirect('accounts:login')
#     else:
#         form = RegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})



class UserLoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/auth/login.html'
    success_url = '/'
    
    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if not user.is_active:
                messages.error(request, 'This user is inactive!')
                return super(UserLoginView, self).form_invalid(form)
            login(request, user)
            # user_login_signal.send(user.__class__, instance=user, request=request)
            try:
                del request.session["guest_user_id"]
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            messages.error(request, 'Invalid username or password!')
        return super(UserLoginView, self).form_invalid(form)
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserLoginView, self).get_context_data(*args, **kwargs)
        context['category_qs']=Category.objects.filter(active=True)
        return context 
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You loged out your account!')
    return redirect('home')
        
            
            
# User Login section
# def user_login(request):

#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None

#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=email, password=password)
#             if user:
#                 login(request, user)
#                 try:
#                     del request.session["guest_user_id"]
#                 except:
#                     pass
#                 if is_safe_url(redirect_path, request.get_host()):
#                     return redirect(redirect_path)
#                 else:
#                     return redirect('/')
#             else:
#                 messages.error(request, 'Invalid username or password!')
#     else:
#         form = LoginForm()
#     return render(request, 'accounts/auth/login.html', {'form': form})



# Guest user register section
def guest_user_register(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if request.method == 'POST':
        form = GuestForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            new_guest_user = GuestEmail.objects.create(email=email)
            request.session["guest_user_id"] = new_guest_user.id
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('accounts:register')
        else:
            redirect("accounts:register")
    else:
        form = GuestForm()
    return render(request, 'accounts/auth/login.html', {'form': form})


# User Account detail 
@login_required
def user_profile_view(request):
    qs = Category.objects.filter(active=True)
    billing_obj, created = BillingProfile.objects.new_or_get(request)
    if created:
        pass
    order_qs = Order.objects.filter(billing_profile=billing_obj)
    created_order = order_qs.filter(status='created')
    shipped_order = order_qs.filter(status='shipped')
    paid_order = order_qs.filter(status='paid')
    canceled_order = order_qs.filter(status='cancel')

    has_card = billing_obj.has_card
    context = {
        'category_qs': qs,
        'order_qs': order_qs,
        'created_order': created_order,
        'shipped_order': shipped_order,
        'paid_order': paid_order,
        'canceled_order': canceled_order,
        'has_card': has_card,
        'billing_obj': billing_obj
    }
    return render(request, 'accounts/profile_detail.html', context)


@login_required
def order_list_view(request):
    qs = Category.objects.filter(active=True)
    billing_obj, created = BillingProfile.objects.new_or_get(request)
    if created:
        pass
    order_qs = Order.objects.filter(billing_profile=billing_obj).exclude(status='created')
    query = request.GET.get('order_search',None)
    if query is not None:
        order_qs = order_qs.filter(Q(order_id__icontains=query))

    context = {
        'category_qs': qs,
        'order_qs': order_qs
    }
    return render(request, 'accounts/order_list.html', context)

@login_required
def order_detail_view(request, order_id):
    qs = Category.objects.filter(active=True)
    billing_obj, created = BillingProfile.objects.new_or_get(request)
    if created:
        pass
    try:
        order_obj = Order.objects.get(order_id=order_id)
    except:
        pass

    context = {
        'category_qs': qs,
        'order_obj': order_obj
    }
    return render(request, 'accounts/order_detail.html', context)

@login_required
def account_settings(request):
    qs = Category.objects.filter(active=True)
    userprofile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        
        user_form = UserEdit(request.POST, instance=request.user)
        profile_form = UserProfileEdit(request.POST, request.FILES, instance=request.user.userprofile )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Accout updated.')
            return redirect("accounts:account_settings")

    else:
        
        user_form = UserEdit(instance=request.user)
        profile_form = UserProfileEdit(instance=request.user.userprofile )

    billing_obj, created = BillingProfile.objects.new_or_get(request)
    has_card = billing_obj.has_card
    context = {
        'category_qs': qs,
        'user_form': user_form,
        'profile_form': profile_form,
        'has_card': has_card,
        'billing_obj': billing_obj
    }

    return render(request, 'accounts/settings.html', context)











