from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import json



def register(request) :
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST' :
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                Customer.objects.create(user=user,name=user.username)
                messages.success(request,'Account was created for ' + str(user))
                return redirect('loginpage')
    context = {
    'form' : form
    }
    return render(request,'ecommerce/register.html',context)

def loginpage(request) :
    if request.user.is_authenticated:
        return redirect('home')
    else :
        if request.method == 'POST' :
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username, password = password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else :
                messages.info(request,'Username OR Password is incorrect')
    context = {
    }
    return render(request,'ecommerce/login.html',context)

def logoutpage(request) :
    logout(request)
    context = {
    }
    return redirect('loginpage')

@login_required(login_url = 'loginpage')
def home(request) :
    if request.user.is_authenticated:
        customer = request.user.customer
        # customer = Customer.objects.create(user = user)
        # print(customer)
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity

        # print(items)
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_quantity' : 0}
        cartItems = order['get_cart_quantity']
    products = Product.objects.all()
    context = {
    'products' : products,
    'cartItems' : cartItems
    }
    return render(request,'ecommerce/home.html',context)

@login_required(login_url = 'loginpage')
def cart(request) :
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity

        print(items)
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_quantity' : 0}
        cartItems = order['get_cart_quantity']
    context = {
    'items' : items,
    'order' : order,
    'cartItems' : cartItems
    }
    return render(request,'ecommerce/cart.html',context)

@login_required(login_url = 'loginpage')
def checkout(request) :
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity

        print(items)
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_quantity' : 0}
        cartItems = order['get_cart_quantity']
    context = {
    'items' : items,
    'order' : order,
    'cartItems' : cartItems
    }
    return render(request,'ecommerce/checkout.html',context)

def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:' ,action)
    print('productId:' ,productId)

    customer = request.user.customer
    print('Customer is  : ', customer)
    product = Product.objects.get(id = productId)
    print('Product is  : ', product)
    order,created = Order.objects.get_or_create(customer = customer,complete = False)
    print('order is  : ', order)
    orderItem,created = OrderItem.objects.get_or_create(order = order, product = product)
    print('orderItem is  : ', orderItem)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0 :
        orderItem.delete()

    return JsonResponse('Item was added',safe = False)

def processorder(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer = customer,complete = False)
        Shipping.objects.create(
        customer = customer,
        order = order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state = data['shipping']['state'],
        zip_code = data['shipping']['zipcode'])

    return JsonResponse('Payment Complete',safe = False)
