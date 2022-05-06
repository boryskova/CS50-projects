from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_auction", views.add_auction, name="new_auction"),
    path("auctions/id=<int:lot_id>", views.auction_page, name="auction_page"),
    path("wishlist", views.wishlist, name="wishlist_page"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:cat_name>&id=<int:cat_id>", views.category_listing, name="category_listing")
]
