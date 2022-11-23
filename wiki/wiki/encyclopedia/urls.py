from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_page, name="page"),
    path("wiki/search_results/", views.search, name="search"),
    path("create_new_page", views.new_entry, name="new_page"),
    path("random", views.random_entry, name="random_page"),
    path("edit_page/<str:entry>", views.edit_entry, name="edit_page")
]
