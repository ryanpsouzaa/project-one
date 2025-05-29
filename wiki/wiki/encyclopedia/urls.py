from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("newpage/", views.new_page, name="new_page"),
    path("search/", views.search, name="search_page"),
    path("similarsearch/<str:title>/", views.similar_search, name="similar_search"),
    path("editpage/<str:title>", views.edit_page, name="edit_page"),
    path("random/", views.random_page, name="random_page"),
    path("<str:title>/", views.get_page, name="get_page")
]
