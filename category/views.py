from django.shortcuts import render

from .models import Category, SubCategory

def category_list(request):
    category_qs = Category.objects.filter(active=True)
    category_obj = Category.objects.get(id=1)
    context = {
        'category_qs': category_qs
    }
    return render(request, 'category/c_list.html', context)


def category_detail(request, pk):
    category = Category.objects.get(id=pk)
    sub_category = category.subcategory_set.all()
    category_qs = Category.objects.filter(active=True)
    context = {
        'category': category, 
        'sub_category': sub_category,
        'category_qs': category_qs
    }
    return render(request, "category/c_detail.html", context)

def sub_category_detail(request, pk):
    sub_category_obj = SubCategory.objects.get(id=pk)
    category_qs = Category.objects.filter(active=True)
    context = {
        'subcategory_obj': sub_category_obj,
        'category_qs': category_qs
    }
    return render(request, "category/s_c_detail.html", context)


