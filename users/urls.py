from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path(
        'login/',
        LoginView.as_view(template_name='users/auth.html',
                          next_page='storage:index'),
        name='login'
    ),
    path(
        "logout/", LogoutView.as_view(template_name="users/logout.html",
                                      next_page='meal_app:index'),
        name="logout"
    ),
    path('password_change/',
         PasswordChangeView.as_view(template_name='users/change_password.html'),
         name='password_change'),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # path('profile/<str:username>/', views.profile, name='profile'),
    # path('profile/<str:username>/plan/<user_plan_id>/', views.plan_user, name='user_plan'),
]
