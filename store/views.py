from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.EmailBackEnd import *
from dashboard.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json

# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    top_deal = Product.objects.filter(top_deal=True)
    flash_sales = Product.objects.filter(flash_sales=True)
    context = {
        'products': products,
        'top_deal': top_deal,
        'flash_sales': flash_sales,
        'categories': categories
    }
    return render(request, 'store/index.html',context)

def category(request, slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=category)
    context = {
        'product': product,
        'categories': categories,
        'category': category
    }
    return render(request, 'store/category.html',context)

def product_detail(request,pk):
    product = Product.objects.get(id=pk)
    similiar_product = Product.objects.filter(category=product.category).exclude(id=product.id)
    context = {
        'product': product,
        'similiar_product': similiar_product
    }
    return render(request, 'store/product_details.html', context)

def search(request):
    if request.method == 'POST':
        kw = request.POST['keyword']
        result = Product.objects.filter(Q(name__icontains=kw) | Q(description__icontains=kw))
        context = {
            'result':result
        }
    return render(request, 'store/search.html', context)

def second_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = EmailBackEnd.authenticate(request,username=email,password=password)
        if user !=None:
            print(user)
            login(request,user)
            if user.user_type=="1":
                return redirect('dashboard:dashboard_home')
            elif user.user_type=="2":
                return redirect('store:home')
            else:
                messages.error(request,"Invalid Login Details")
        else:
            messages.error(request,"Invalid Login Details")
            return redirect("user:do_login")


@login_required(login_url="do_login")   
def cart(request):
    customer = Customer.objects.get(admin=request.user)
    cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
    cartitems = cart.cartitems_set.all()
    context = {
        'cart': cart,
        'cartitems': cartitems
    }
    return render(request, 'store/cart.html', context)

def update_cart(request):
    return JsonResponse('it is working', safe=False)