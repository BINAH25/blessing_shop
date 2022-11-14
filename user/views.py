from django.shortcuts import render, redirect
from django.contrib import messages
from dashboard.models import *
from django.contrib.auth import authenticate, login, logout
from .EmailBackEnd import *
from django.views.generic import DetailView

# Create your views here.
def register(request):
    if request.method =="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        #CHECK IF USERNAME ALREADY EXIST
        if CustomUser.objects.filter(username=username):
            messages.error(request, "Username Already Exist")
            return redirect(request.META.get("HTTP_REFERER"))
        
        #CHECK IF EMAIL ALREADY EXIST
        if CustomUser.objects.filter(email=email):
            messages.error(request, "Email Already Exist")
            return redirect(request.META.get("HTTP_REFERER"))

        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
            user.save()
            messages.success(request,"Account Created Successfully")
            return redirect('do_login')
        except:
            messages.error(request,"Registration Failed ")
            return redirect('register')

    return render(request,'user/register.html')

def do_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = EmailBackEnd.authenticate(request,username=email,password=password)
        if user !=None:
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

    return render(request, 'user/login.html')

def logout_user(request):
    logout(request)
    return redirect("store:home")

def change_password_user(request):
    if request.method == 'POST':
        current  = request.POST['current']
        new  = request.POST['new']
        confirm  = request.POST['confirm']
        if new != confirm:
            messages.error(request, " new password and confirm new password mismatch")
            return redirect('user_orders')
        user = EmailBackEnd.authenticate(request,username=request.user.email,password=current)
        if(user):
            user.set_password(new)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect('store:home')
        else:
            messages.error(request, "Incorrect Curent Password")
            return redirect('user_orders')

def user_orders(request):
    customer = Customer.objects.get(admin=request.user)
    orders = Order.objects.filter(customer=customer)
    context = {
        'orders': orders
    }
    return render(request, 'user/orders.html',context)

def user_profile(request):
    return render(request, 'user/user_profile.html')

def user_profile_update(request):
    return render(request, 'user_profile_update.html')
class CustomerOrderDetail(DetailView):
    template_name = 'user/user_order_detail.html'
    model = Order
    context_object_name = 'ord_obj'
