from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("newpage/", views.new_page, name="new_page"),
    path("<str:title>/", views.get_page, name="get_page")
]
