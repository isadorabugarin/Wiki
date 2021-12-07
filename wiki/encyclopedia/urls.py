from django.urls import path

from . import views

app_name="tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("query", views.query, name="query"),
    path("new", views.new, name="new"),
    path("<str:title>", views.title, name="title")

]
