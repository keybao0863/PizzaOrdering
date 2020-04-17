from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    # Check is user logged in
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message":None})

    #If logged in
    context = {
        "user" : request.user
    }
    return render(request, "orders/user.html", context)

def login_view(request):
    # Render view
    if request.method=='GET':
        return render(request, "orders/login.html")

    # Authenticate
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication succeeds
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message":"invalid credentials."})

def logout_view(request):
    logout(request)
    print("logged out")
    return render(request, "orders/login.html", {"message": "Logged out."})

def signup_view(request):

    # Render view
    if request.method=='GET':
        return render(request, "orders/signup.html")

    #Create new user
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]

    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return render(request, "orders/login.html", {"message":"Signup successful"})

@login_required(login_url="/login")
def menu_view(request):
    # Make sure there is a logged in user
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message":None})

    # Display menu items
    items = Menu_item.objects.all()
    toppings = Topping.objects.all()
    context = {
        "items": items,
        "toppings": toppings
    }

    return render(request, "orders/menu.html", context)

def add_to_cart(request, item_id):

    #Retrieve menu item
    item = Menu_item.objects.filter(pk=item_id).first()

    #Check if user already has an open order. If so, append to that order
    current_user = request.user
    cur_order = Order.objects.filter(user=current_user, is_ordered=False).first()

    #If order does not exit, create order
    if(not cur_order):
        cur_order = Order(user=current_user)
        cur_order.save()





    # Append items to the open order
    order_item = Order_item(order = cur_order, Menu_item = item, quantity=1)
    order_item.save()
    #Add toppings, if any
    print("topping number" ,item.topping_number)
    if(item.topping_number>0):
        topping = Topping.objects.filter(name= request.POST['topping1']).first()
        print(topping)
        order_item.toppings.add(topping)
    if(item.topping_number>1):
        topping = Topping.objects.filter(name= request.POST['topping2']).first()
        order_item.toppings.add(topping)
    if(item.topping_number>2):
        topping = Topping.objects.filter(name= request.POST['topping3']).first()
        order_item.toppings.add(topping)

    order_item.save()

    # Show message and return view
    messages.info(request, "Successfully added to cart")
    return redirect(reverse(menu_view))

@login_required(login_url="/login")
def cart_view(request):

    #Get current user
    current_user = request.user

    #Check if user has an order
    cur_order = Order.objects.filter(user=current_user, is_ordered=False).first()

    #If not return error
    if(not cur_order):
        messages.info(request, "You do not have any open order.")
        return redirect(reverse(menu_view))

    #If user has a open order, calculate price and display it
    order_items = Order_item.objects.filter(order = cur_order).all()
    sum = 0
    for item in order_items:
        sum+= item.Menu_item.price * item.quantity

    #Display
    context = {
        "order_items":order_items,
        "price":sum
    }
    return render(request, "orders/cart.html", context)

@login_required(login_url="/login")
def place_order(request):
    
