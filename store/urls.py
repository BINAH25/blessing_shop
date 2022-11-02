from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("second_login", views.second_login, name="second_login"),
    path('category/<str:slug>', views.category, name = 'category'),
    path('product_detail/<int:pk>', views.product_detail, name = 'product_detail'),
    path('search', views.search, name = 'search'),

]