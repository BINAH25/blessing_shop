from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#app_name = "user"

urlpatterns = [
    path("", views.register, name="register"),
    path("do_login", views.do_login, name="do_login"),
    path("logout_user", views.logout_user, name="logout_user"),
    path("user_orders", views.user_orders, name="user_orders"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("change_password_user", views.change_password_user, name="change_password_user"),
    path ('user/order-<int:pk>/', views.CustomerOrderDetail.as_view(), name='customerorderdetail'),

    # ******************* RESET PASSWORD VIEW *****************************
    path('password_reset', auth_views.PasswordResetView.as_view(
        template_name='user/reset_password.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(
        template_name='user/reset_password_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/reset_password_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/reset_password_complete.html'), name='password_reset_complete'),

]