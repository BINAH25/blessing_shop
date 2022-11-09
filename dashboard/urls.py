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
    path("pending_orders", views.pending_orders, name="pending_orders"),
    path("completed_orders", views.completed_orders, name="completed_orders"),
    path("canceled_orders", views.canceled_orders, name="canceled_orders"),
    path('order-detail/<int:pk>/', views.AdminOrderDetailView.as_view(), name='dashboard-order-detail'),
    path("order_completed/<int:pk>/", views.order_completed, name="order_completed"),
    path("order_cancel/<int:pk>/", views.order_cancel, name="order_cancel"),
    path("all_customer", views.all_customer, name="all_customer"),
    path("change_password", views.change_password, name="change_password"),
    
]
