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
import time
from django.views.generic import View, DetailView

# Create your views here.

def dashboard_home(request):
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    order_completed = Order.objects.filter(order_status=1).count()
    order_canceled = Order.objects.filter(order_status=2).count()
    customers = Customer.objects.all().count()
    orders = Order.objects.all().count()

    time_in_hrs = int(time.strftime("%H"))
    if 0 < time_in_hrs < 12:
        greeting = "Good Morning!" 
    elif 12 <= time_in_hrs < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    context = {
        'greeting': greeting,
        'notifications': notifications,
        'notifications_details':notifications_details,
        'customers': customers,
        'orders': orders,
        'order_canceled': order_canceled,
        'order_completed': order_completed
    }
    return render(request, 'dashboard/home.html', context)


def add_category(request):
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    if request.method =="POST":
        title=request.POST.get("title")
        slug=request.POST.get("slug")
        category = Category(title=title, slug=slug)
        category.save()
        messages.success(request,"category Added Successfully ")
        return redirect('dashboard:add_category')
    context = {
        'notifications': notifications,
        'notifications_details':notifications_details
    }   
    return render(request, 'dashboard/add_category.html', context)

def add_product(request):
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'notifications': notifications,
        'notifications_details':notifications_details
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
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    context = {
        'products': products,
        'categories':categories,
        'notifications': notifications,
        'notifications_details':notifications_details
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
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    context = {
        'product': product,
        'categories': categories,
        'notifications': notifications,
        'notifications_details':notifications_details
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

def pending_orders(request):
    all_pending_orders = Order.objects.filter(order_status=0).order_by('-id')
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    context = {
        'all_pending_orders': all_pending_orders,
        'notifications': notifications,
        'notifications_details':notifications_details
    }
    return render(request, 'dashboard/pending_orders.html', context)

def completed_orders(request):
    all_completed_orders = Order.objects.filter(order_status=1).order_by('-id')
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    context = {
        'all_completed_orders': all_completed_orders,
        'notifications': notifications,
        'notifications_details':notifications_details
    }
    return render(request, 'dashboard/completed_orders.html', context)

def canceled_orders(request):
    all_canceled_orders = Order.objects.filter(order_status=2).order_by('-id')
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    context = {
        'all_canceled_orders': all_canceled_orders,
        'notifications': notifications,
        'notifications_details':notifications_details
    }
    return render(request, 'dashboard/canceled_orders.html', context)

def order_completed(request,pk):
    order = Order.objects.get(id=pk)
    order.order_status = 1
    order.save()
    return redirect('dashboard:pending_orders')

def order_cancel(request,pk):
    order = Order.objects.get(id=pk)
    order.order_status = 2
    order.save()
    return redirect('dashboard:pending_orders')

class AdminOrderDetailView(DetailView):
    template_name = 'dashboard/pending_orders_detail.html'
    model = Order
    context_object_name = 'ord_obj'
    
def all_customer(request):
    customers = Customer.objects.all().order_by('-id')
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')

    context = {
        'customers': customers,
        'notifications': notifications,
        'notifications_details':notifications_details
    }
    return render(request, 'dashboard/customers.html', context)

def change_password(request):
    if request.method == 'POST':
        current  = request.POST['current']
        new  = request.POST['new']
        confirm  = request.POST['confirm']
        if new != confirm:
            messages.error(request, " new password and confirm new password mismatch")
            return redirect(request.META.get("HTTP_REFERER"))
        user = EmailBackEnd.authenticate(request,username=request.user.email,password=current)
        if(user):
            user.set_password(new)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "Incorrect Curent Password")
            return redirect(request.META.get("HTTP_REFERER"))

def admin_profile(request):
    notifications = Order.objects.filter(order_status=0).count()
    notifications_details = Order.objects.filter(order_status=0).order_by('-id')
    context = {
        'notifications': notifications,
        'notifications_details':notifications_details
    }
    return render(request, 'dashboard/admin_profile.html',context)

def admin_update_profile(request):
    return render