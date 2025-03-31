from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views

route = DefaultRouter()

route.register("videos", views.VideoAPIView, basename="videos")
route.register("videoDetails", views.VideoDetailsAPIView, basename="video_details")
route.register("search", views.SearchAPIView, basename="search")
route.register("cartegory", views.CartegoryAPIView, basename="cartegory")
route.register("review", views.ReviewAPIView, basename="review")
route.register("like", views.LikeAPIView, basename="like")
route.register("purchased", views.PurchasedAPIView, basename="purchased")
route.register("download", views.DownloadHistoryAPIView, basename="Download")
route.register("deposit_history", views.DepositHistoryAPIView, basename="DepositHistory")
route.register("onwatch", views.OnwatchAPIView, basename="Onwatch")
route.register("cart", views.CartAPIView, basename="cart")
route.register("profile", views.ProfileAPIView, basename="profile")
route.register("members", views.MembersAPIView, basename="members")
route.register("message", views.MessageAPIView, basename="message")
route.register("notification", views.NotificationAPIView, basename="notification")
urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('deposit/', views.deposit, name='deposit'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('password_reset/request/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset/reset/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("info/", views.UserInfoAPIView.as_view(), name="user-info"),
    path("", include(route.urls))
]
