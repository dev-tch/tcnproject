from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "tcn"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="tcn/registration/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", TemplateView.as_view(template_name="tcn/home.html"), name="home"),
]
