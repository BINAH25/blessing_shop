from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.EmailBackEnd import *
from dashboard.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json
from .forms import *
from django.contrib import messages

# Create your views here.
def home(request):
    reviews = Review.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    top_deal = Product.objects.filter(top_deal=True)
    flash_sales = Product.objects.filter(flash_sales=True)
    if request.user.is_authenticated:
        customer = Customer.objects.get(admin=request.user)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'num_of_items': 0}

    context = {
        'products': products,
        'top_deal': top_deal,
        'flash_sales': flash_sales,
        'categories': categories,
        'cart': cart,
        'cartitems': cartitems,
        'reviews': reviews
    }
    return render(request, 'store/index.html',context)

def category(request, slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=category)
    if request.user.is_authenticated:
        customer = Customer.objects.get(admin=request.user)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'num_of_items': 0}

    context = {
        'product': product,
        'categories': categories,
        'category': category,
        'cart': cart,
        'cartitems': cartitems
    }
    return render(request, 'store/category.html',context)

def product_detail(request,pk):
    product = Product.objects.get(id=pk)
    similiar_product = Product.objects.filter(category=product.category).exclude(id=product.id)
    if request.user.is_authenticated:
        customer = Customer.objects.get(admin=request.user)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'num_of_items': 0}

    context = {
        'product': product,
        'similiar_product': similiar_product,
        'cart': cart,
        'cartitems': cartitems
    }
    return render(request, 'store/product_details.html', context)

def search(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(admin=request.user)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'num_of_items': 0}

    if request.method == 'POST':
        kw = request.POST['keyword']
        result = Product.objects.filter(Q(name__icontains=kw) | Q(description__icontains=kw))
        
        context = {
            'result':result,
            'cart': cart,
            'cartitems': cartitems
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
            return redirect("do_login")


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
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(admin=request.user)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)

        if action == 'add':
            cartitems.quantity += 1
        cartitems.save()
        
        msg = {
            'quantity': cart.num_of_items
        }

    else:
        return redirect('do_login')   
    return JsonResponse(msg,safe=False)

def update_quantity(request):
    data = json.loads(request.body)
    value = int(data['in_val'])
    product_id = data['p_id']
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(admin=request.user)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)
        cartitems.quantity = value
        cartitems.save()

        msg = {
            'subtotal': cartitems.subTotal,
            'quantity': cart.num_of_items,
            'total': cart.cart_total
        }

    return JsonResponse(msg, safe=False)

def delete_item(request):
    data = json.loads(request.body)
    product_id = data['del_id']
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(admin=request.user)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems = Cartitems.objects.filter(product=product, cart=cart)
        cartitems.delete()
    return JsonResponse(safe=False)

def check_out(request):
    customer = Customer.objects.get(admin=request.user)
    cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
    cartitems = cart.cartitems_set.all()
    context = {
        'cart': cart,
        'cartitems': cartitems
    }
    return render(request, 'store/checkout.html', context)


def order(request):
    customer = Customer.objects.get(admin=request.user)
    cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
    cart.completed = True
    cart.save()
    if request.method == "POST":
        ordered_by = request.POST['ordered_by']
        location = request.POST['location']
        mobile = request.POST['mobile']
        email = request.POST['email']
        order = Order(ordered_by=ordered_by,location=location,mobile=mobile,email=email,cart=cart,order_status=0,customer=customer)
        order.save()
        messages.success(request, f" {ordered_by}, Your order(s) have been placed successfully.")
        return redirect('store:home')

def blog(request):
    blogs = Blog.objects.all().order_by('-id')
    context = {
        'blogs': blogs
    }
    return render(request, 'store/blog.html', context)