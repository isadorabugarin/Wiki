import secrets

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
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(content),
            "entry": entry,
            "form": SearchForm()
        })

#INDEX PAGE
def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
        })

#SEARCH PAGE
class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

def search(request):
    if request.method == "GET":
        markdowner = Markdown()
        form = SearchForm(request.GET)
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
                             "form": SearchForm()
                        })
            else:
                return render(request, "encyclopedia/search.html", {
                    "entry": markdowner.convert(content),
                    "form": SearchForm()
                    })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })



#NEW ENTRY PAGE
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-g'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8','rows':10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            markdowner = Markdown()
            title = form.cleaned_data["title"].capitalize()
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True ):
                util.save_entry(title,content)
                return render(request, "encyclopedia/entry.html", {
                    "content": markdowner.convert(content),
                    "form":SearchForm()
                })
            else:
                return render(request, "encyclopedia/new.html", {
                        "form2": form,
                        "entry_exists": True,
                        "entry": title,
                        "form": SearchForm()
                })
        else:
            return render(request, "encyclopedia/new.html", {
            "form2": form,
            "entry_exists": False,
            "form": SearchForm()
            })
    else:
        return render(request, "encyclopedia/new.html", {
        "form2": NewEntryForm(),
        "form": SearchForm()
        })

#EDIT ENTRY PAGE
def edit(request, entry):
    content = util.get_entry(entry)
    if content is None:
        return render(request, "encyclopedia/notfound.html", {
            "entry":entry,
            "form": SearchForm()
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["content"].initial = content
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/new.html", {
            "form2":form,
            "form": SearchForm(),
            "edit":form.fields["edit"].initial,
            "entry": form.fields["title"].initial

        })
#RANDOM PAGE
def random(request):
    markdowner = Markdown()
    entries = util.list_entries()
    random = secrets.choice(entries)
    content = util.get_entry(random)
    return render(request, "encyclopedia/entry.html", {
	"entry":random,
    "content": markdowner.convert(content),
    "form": SearchForm()
    })


