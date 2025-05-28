from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content",widget=forms.Textarea)

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/create-page.html", {
                    "form" : form,
                    "message" : f"Title: {title} is already created"
                })
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            #redirecionamento
            return redirect("encyclopedia:get_page", title=title)
        else:
            return render(request, "encyclopedia/create-page.html", {
                "form": form
            })
    return render(request, "encyclopedia/create-page.html", {
        "form": NewPageForm()
    })

def get_page(request, title):
    page = util.get_entry(title)
    return render(request, "encyclopedia/page.html", {
        "page" : page
    })



