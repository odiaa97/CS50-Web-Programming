from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_entry', views.add_entry, name='add_entry'),
    path('delete_entry', views.delete_entry, name='delete_entry'),
    path('wiki/random_title', views.random_entry, name='random_entry'),
    path('wiki/<str:title>', views.get_entry, name='TITLE'),
]
