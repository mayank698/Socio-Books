from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.signup, name="signup"),
    path("login", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("settings", views.settings, name="settings"),
    path("upload", views.upload, name="upload"),
    path("likes", views.likes, name="likes"),
    path("follow", views.follow, name="follow"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("search", views.search, name="search"),
]
