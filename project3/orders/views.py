from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .models import Category, Item
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import Order

# Create your views here.


def order(request):
    context = {
        "pizza": Order.objects.filter(category="Pizza"),
        "drinks": Order.objects.filter(category="Drinks"),
        "dessert": Order.objects.filter(category="Dessert"),
        "salad": Order.objects.filter(category="Salad"),
        "hot_drinks": Order.objects.filter(category="Hot drinks"),
    }
    return render(request, "orders/shopcart.html", context)


def add(request):
    name = request.POST['name']
    price = int(request.POST['price'])
    category = request.POST['category']
    Order.objects.create(name=name, category=category, price=price)
    return HttpResponse("Done")


def remove(request):
    Order.objects.all().delete()
    return render(request, "orders/index.html")


def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    else:
        context = {
            "menu": Category.objects.all(),
            "items": Item.objects.all(),
            "username": request.user.username
        }
        return render(request, "orders/index.html", context)


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html",
{"message": "Invalid Credentials!", "category": "danger"})


def register_view(request):
    return render(request, "orders/register.html", {"message": None, "category": None})


def register(request):
    username = request.POST["username"]
    password = request.POST["password"]
    re_password = request.POST["repassword"]
    email = request.POST["email"]
    user = User.objects.filter(username=username)
    if not user:
        if password == re_password:
            User.objects.create_user(username, email, password)
            return render(request, "orders/login.html", {"message": "User created successfully", "category": "success"})
        else:
            return render(request, "orders/register.html", {"message": "Invalid password", "category": "danger"})
    else:
        return render(request, "orders/register.html", {"message": "Username already exists", "category": "danger"})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out.", "category": "success"})


