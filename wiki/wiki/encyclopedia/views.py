from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    page = util.get_entry(entry)

    if page != None:
        page = Markdown().convert(page)
    else:
        pass

    return render(request, "encyclopedia/page.html", {
        "page_title": entry,
        "page": page
    })

def search(request):
    search = request.GET.get('q')
    entries = util.list_entries()

    if any(e for e in entries if search.lower() == e.lower()):
        page = Markdown().convert(util.get_entry(search))
        return render(request, "encyclopedia/page.html", {
            "page_title": search,
            "page": page
        })
    else:
        entries = [e for e in entries if search.lower() in e.lower()]
        return render(request, "encyclopedia/search_page.html", {
            "entries" : entries
        })
        

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title", widget=forms.TextInput)
    content = forms.CharField(label='', widget=forms.Textarea)

def new_entry(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)       
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"] 
            entries = util.list_entries()
            if any(e for e in entries if title.lower() == e.lower()):
                messages.add_message(request, messages.INFO, f'The \"{title.capitalize()}\" page already exists!')
            else:  
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("page", args=[title,]))
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })

class EditPageForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea)

def edit_entry(request, entry):
    page = util.get_entry(entry)

    if request.method == "POST":
        form = EditPageForm(request.POST)       
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("page", args=[entry,]))
        else:
            form = EditPageForm(initial={"content": page})
            return render(request, "encyclopedia/edit_page.html", {
                "page_title": entry,
                "form": form
            })

    form = EditPageForm(initial={"content": page})
    return render(request, "encyclopedia/edit_page.html", {
        "page_title": entry,
        "form": form
    })
    

def random_entry(request):
    entries = util.list_entries()
    random_title = random.choice(entries)

    return HttpResponseRedirect(reverse("page", args=[random_title,]))


    
    
    






