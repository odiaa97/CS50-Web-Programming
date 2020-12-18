from django.shortcuts import render, redirect
from django import forms
from markdown2 import markdown
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


def search(request):
    q = request.GET.get('q')
    if q in util.list_entries():
        return redirect('encyclopedia:entry', title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})


def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        entry = "## Page was not found"
    entry = markdown(entry)
    return render(request, f"encyclopedia/entry.html", {
        "entry": entry, 
        "title": title
    })
    


