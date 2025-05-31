from importlib.resources import contents

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.template.defaultfilters import length

from . import util

import markdown2

import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if not title.strip() or not content.strip():
            return render(request, "encyclopedia/create-page.html", {
                "error" : "Title and Content cannot be empty",
                "title" : title,
                "content" : content
            })
        if title in util.list_entries():
            return render(request, "encyclopedia/create-page.html", {
                "error" : f"Title: {title} is already created",
                "title" : title,
                "content" : request.POST.get("content")
            })
        util.save_entry(title, content)
        return redirect("encyclopedia:get_page", title=title)
    else:
        return render(request, "encyclopedia/create-page.html")

def get_page(request, title):
    page_markdown = util.get_entry(title)
    if page_markdown is None:
        return redirect("encyclopedia:similar_search", title=title)
    else:
        page_html = markdown2.markdown(f"{page_markdown}")
        return render(request, "encyclopedia/page.html", {
            "page_title": title,
            "page_content": page_html,
        })


def search(request):
    title = request.GET.get("q")
    return redirect("encyclopedia:get_page", title=title)


def similar_search(request, title):
    similar_search = []
    for entry in util.list_entries():
        if title.lower() in entry.lower():
            similar_search.append(entry)

    if len(similar_search) == 0:
        return render(request, "encyclopedia/error.html", {
            "error": f"Page {title} not found"
        })

    else:
        return render(request, "encyclopedia/similar-search.html", {
            "similar_entries": similar_search
        })


def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        if not content.strip():
            return render(request, "encyclopedia/edit-page.html", {
                "error" : "Content cannot be empty",
                "content" : util.get_entry(title),
                "title" : title
            })
        util.save_entry(title, content)
        return redirect("encyclopedia:get_page", title=title)

    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit-page.html", {
            "title": title,
            "content" : content
        })
#todo editar edit-page, create-page e estilizar o resto
def random_page(request):
    list_entries = util.list_entries()
    choice = random.choice(list_entries)
    return redirect("encyclopedia:get_page", title=choice)
