from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

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
