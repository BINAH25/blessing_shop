from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.EmailBackEnd import *
from dashboard.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# Create your views here.

def dashboard_home(request):
    return render(request, 'dashboard/home.html')


def add_category(request):
    if request.method =="POST":
        title=request.POST.get("title")
        slug=request.POST.get("slug")
        category = Category(title=title, slug=slug)
        category.save()
        messages.success(request,"category Added Successfully ")
        return redirect('dashboard:add_category')
        
    return render(request, 'dashboard/add_category.html')

def add_product(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    if request.method =="POST":
        name=request.POST.get("name")
        description=request.POST.get("description")
        price=request.POST.get("price")
        image=request.FILES.get("image")
        category_id=request.POST.get("category")
        slug=request.POST.get("slug")
        top_deal=request.POST.get("top_deal") or False
        flash_sales=request.POST.get("flash_sales") or False
        category=Category.objects.get(id=category_id)
        try:
            product=Product(name=name,description=description,price=price,image=image,category=category,slug=slug,top_deal=top_deal,flash_sales=flash_sales)
            product.save()
            messages.success(request,"Product Added Successfully ")
            return redirect('dashboard:add_product')
        except:
            messages.error(request,"Failed to Add Product")
            return redirect('dashboard:add_product')

    return render(request, 'dashboard/add_product.html',context)

def all_product(request):
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories':categories
    }
    if request.method =="POST":
        name=request.POST.get("name")
        description=request.POST.get("description")
        price=request.POST.get("price")
        image=request.FILES.get("image")
        category_id=request.POST.get("category")
        slug=request.POST.get("slug")
        top_deal=request.POST.get("top_deal") or False
        flash_sales=request.POST.get("flash_sales") or False
        category=Category.objects.get(id=category_id)
        try:
            product=Product(name=name,description=description,price=price,image=image,category=category,slug=slug,top_deal=top_deal,flash_sales=flash_sales)
            product.save()
            messages.success(request,"Product Added Successfully ")
            return redirect('dashboard:all_product')
        except:
            messages.error(request,"Failed to Add Product")
            return redirect('dashboard:all_product')

    return render(request, 'dashboard/all_product.html', context)

def edit_product(request,pk):
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()

    context = {
        'product': product,
        'categories': categories
    }
    if request.method =="POST":
        name=request.POST.get("name")
        description=request.POST.get("description")
        price=request.POST.get("price")
        image=request.FILES.get("image")
        category_id=request.POST.get("category")
        slug=request.POST.get("slug")
        top_deal=request.POST.get("top_deal")
        flash_sales=request.POST.get("flash_sales")
        category=Category.objects.get(id=category_id)
        try:
            product.name = name
            product.description = description
            product.price = price
            product.image = image
            product.category = category
            product.slug = slug
            product.top_deal = top_deal
            product.flash_sales = flash_sales
            product.save()
            messages.success(request,"Product Edited Successfully ")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request,"Failed to Edit Product")
            return redirect(request.META.get("HTTP_REFERER"))

    return render(request, 'dashboard/edit_product.html', context)

def delete_product(request,pk):
    product=Product.objects.get(id=pk)
    try:
        product.delete()
        messages.success(request,"Product Deleted Successfully")
        return redirect('dashboard:all_product')
    except:
        messages.error(request,"Failed to Delete Product")
        return redirect('dashboard:all_product')
            

def dashboard_search(request):
    if request.method == 'POST':
        kw = request.POST['keyword']
        product = Product.objects.filter(Q(name__icontains=kw) | Q(description__icontains=kw))
        context = {
            'product':product
        }
    return render(request, 'dashboard/dashboard_search.html', context)