"""
URL configuration for flix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path("", views.home, name="homePage"),
    path("multi-media/" , include("multimedia.urls")),
    # path("movies/", views.moviesAndSeries, name="moviesAndSeries"),
    path("mp4/", views.moviesAndSeries, name="moviesAndSeries"),
    path("membership/", include("Members.urls")),
    path("admins/", views.admins, name="admins"),
    path("message/", views.message, name="messages"),
    path("cart/", views.cart, name="cart"),
    path("admins/addVideo/", views.addVideo, name="addVideo"),
    path("play/", views.play, name="play"),
    path("deposit/", views.deposit, name="deposit"),
    path("download/", views.download, name="download"),
    path("removeCart/", views.removeCart, name = "removeCart"),
    path("activate/", views.activate, name="activate"),
    path("stk/", views.stkCallback, name="stkCallBack"),
    path("search/", views.search, name="Search"),
    path("deactivatePay/", views.cancelPurchase, name="cancelPurcharse")
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


admin.site.site_header = "Flixshow Admin"  # Default: "Django Administration"
admin.site.index_title = "Dashboard"  # Default: "Site administration"
admin.site.site_title = "FlixShow"  # Default: "Django site admin"