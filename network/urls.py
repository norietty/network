
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<username>", views.profile, name="profile"),
    path("following", views.follow, name="follow"),
    path("addpost", views.add_post, name="add_post"),
    path("update", views.update, name="update"),
    path("update_post", views.update_post, name="update_post"),
    path("update_follow", views.update_follow, name="update_follow")

]
