from django.urls import path
from . import views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.contrib.auth import views as auth_views


app_name="accounts"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("confirm/<uuid:token>/", views.confirm_email, name="confirm_email"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<uuid:token>/", views.reset_password, name="reset_password"),
]