from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("second_login", views.second_login, name="second_login"),
    path('category/<str:slug>', views.category, name = 'category'),
    path('product_detail/<int:pk>', views.product_detail, name = 'product_detail'),
    path('search', views.search, name = 'search'),
    path('cart', views.cart, name = 'cart'),
    path('update_cart', views.update_cart, name = 'update_cart'),
    path('update_quantity', views.update_quantity, name = 'update_quantity'),
    path('delete_item', views.delete_item, name = 'delete_item'),
    path('check_out', views.check_out, name = 'check_out'),
    path('order', views.order, name = 'order'),
    path('blog', views.blog, name = 'blog'),

]