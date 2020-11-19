from django.shortcuts import render
from django import forms
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    return render(request, f"encyclopedia/entry.html",{
        "entry": util.get_entry(title),
        "title": title
    })

def add_entry(request):
    if request.method == 'POST':
        print("POST Request")
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
    return render(request, f"encyclopedia/add_entry.html")

def delete_entry(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        util.delete_entry(title)
    return render(request, f"encyclopedia/delete_entry.html")

def random_entry(request):
    random_number = random.randint(0, len(util.list_entries()) - 1)
    entries = util.list_entries()
    title = entries[random_number]
    entry = util.get_entry(title)
    return render(request, f"encyclopedia/entry.html",{
        "entry": entry,
        "title": title
    })
    


