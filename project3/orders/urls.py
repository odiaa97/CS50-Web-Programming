from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register_view", views.register_view, name="register_view"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("order", views.order, name="order"),
    path("add", views.add, name="add"),
    path("remove", views.remove, name="remove")
]
