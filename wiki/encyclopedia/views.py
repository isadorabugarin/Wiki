from django import forms
from django.shortcuts import render
from markdown2 import Markdown
from . import util

#ENTRY PAGE
def entry(request,entry):
    markdowner = Markdown()
    content = util.get_entry(entry)
    if content is None:
        return render(request, "encyclopedia/notfound.html", {
            "entry": entry,
            "form": NewTaskForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(content),
            "entry": entry,
            "form": NewTaskForm()
        })

#INDEX PAGE
def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewTaskForm()
        })

#SEARCH PAGE
class NewTaskForm(forms.Form):
    search = forms.CharField(label="Search")


def search(request):
    if request.method == "GET":
        markdowner = Markdown()
        form = NewTaskForm(request.GET)
        if form.is_valid():
            value = form.cleaned_data["search"]
            content = util.get_entry(value)
            if content is None:
                subStringEntries = []
                for entry in util.list_entries():
                    if value.upper() in entry.upper():
                        subStringEntries.append(entry)
                        return render(request, "encyclopedia/index.html", {
                        "entries": subStringEntries,
                        "searching": True,
                        "value": value,
                        "form": form
                        })
                return render(request, "encyclopedia/notfound.html", {
                            "entry":value,
                             "form": form
                        })
            else:
                return render(request, "encyclopedia/search.html", {
                    "entry": markdowner.convert(content),
                    "form": form
                    })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })



#NEW ENTRY PAGE
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        return render(request, "encyclopedia/new.html", {
            "form": form
        })
    return render(request, "encyclopedia/new.html",{
        "form": NewEntryForm()
    })

#EDIT ENTRY PAGE

#RANDOM PAGE



