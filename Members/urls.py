from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("register/",views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("setting/", views.setting, name="setting"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    
]
