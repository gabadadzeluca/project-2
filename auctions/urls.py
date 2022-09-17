from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inactive/", views.inactive, name="inactive"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("wishlist/", views.wishlist, name="wishlist"),
]
