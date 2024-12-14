from django.urls import path
from . import views

urlpatterns = [
    path("tvShows/" , views.types, name="tvShows"),
    path("movies/" , views.types, name="movies"),
    path("music/" , views.types, name="music"),
    path("cart/", views.cart, name="cart"),
   
]
