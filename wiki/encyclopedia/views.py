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
    entry = forms.CharField(label="Entry", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-g'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8','rows':10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True ):
                util.save_entry(title,content)
                return render(request, "encyclopedia/entry.html", {
                    "content": content,
                    "form":SearchForm()
                })
            else:
                return render(request, "encyclopedia/new.html", {
                        "form2": form,
                        "existing": True,
                        "entry": title,
                        "form": SearchForm()
                })
        else:
            return render(request, "encyclopedia/new.html", {
            "form2": form,
            "existing": False,
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
        return render(request, "encyclopedia.notfound.html", {
            "entry":entry
        })
    else:
        form = NewEntryForm()
        form.fields["entry"].initial = entry
        form.fields["entry"].widget = forms.HiddenInput()
        form.fields["entry"].initial = content
        form.fields["entry"].initial = True
        return render(request, "encyclopedia/new.html", {
            "form2":form,
            "edit":form.fields["edit"].initial,
            "entry": form.fields["entry"].initial

        })
#RANDOM PAGE



