from django import forms
from django.shortcuts import render

from . import util



class NewTaskForm(forms.Form):
    query = forms.CharField(label="Search")

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")

def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewTaskForm()
        })

def title(request,title):
    return render(request, "encyclopedia/wiki.html", {
        "title":title,
        "entry": util.get_entry(title),
        "form": NewTaskForm()
        })

def query(request):
    if request.method == "GET":
        form = NewTaskForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            return render(request, "encyclopedia/query.html", {
                "query": query,
                "entry": util.get_entry(query),
                "form": NewTaskForm()
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    return render(request, "encyclopedia/query.html", {
        "form": NewTaskForm()
    })



def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        return render(request, "encyclopedia/new.html", {
            "form": form
        })
    return render(request, "encyclopedia/new.html",{
        "form": NewEntryForm()
    })




