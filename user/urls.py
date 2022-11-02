from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#app_name = "user"

urlpatterns = [
    path("", views.register, name="register"),
    path("do_login", views.do_login, name="do_login"),
    path("logout_user", views.logout_user, name="logout_user"),
    
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