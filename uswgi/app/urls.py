from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("check_repo", views.check_repo, name="check_repo")
]