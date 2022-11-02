from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    path("add_category", views.add_category, name="add_category"),
    path("add_product", views.add_product, name="add_product"),
    path("all_product", views.all_product, name="all_product"),
    path("edit_product/<int:pk>", views.edit_product, name="edit_product"),
    path("delete_product/<int:pk>", views.delete_product, name="delete_product"),
    path("dashboard_search", views.dashboard_search, name="dashboard_search"),
    
]
