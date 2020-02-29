from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from category.models import Category
import json
# Home page

category_list = {}
def home_page(request):
    category_qs = Category.objects.filter(active=True)
    context = {
        'title': 'Welcome to our site!',
        'category_qs': category_qs
    }
    return render(request, 'home.html', context)

# About page
def about_page(request):
    c_qs = Category.objects.filter(active=True)
    context = {
        'category_qs': c_qs
    }
    return render(request, 'about.html', context)


# Contact section
def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('full_name'))
            print(form.cleaned_data.get('email'))
            print(form.cleaned_data.get('message'))

            messages.success(request, 'Your information successfully sent!')
            return redirect("/")
        else:
            messages.warning(request, 'Your information is wrong!')
    else:
        form = ContactForm()
    
    c_qs = Category.objects.filter(active=True)
    context = {
        "category_qs": c_qs,
        'form': form
    }
    return render(request, 'contact_page.html', context)


def privacy_policy(request):
    c_qs = Category.objects.filter(active=True)
    context = {
        "category_qs": c_qs,
    }

    return render(request, "privacy_policy.html", context)







