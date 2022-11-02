from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.register, name="register"),
    path("do_login", views.do_login, name="do_login"),
    path("logout_user", views.logout_user, name="logout_user"),
    
]