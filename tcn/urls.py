from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from . import views_api
app_name = "tcn"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="tcn/registration/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", TemplateView.as_view(template_name="tcn/home.html"), name="home"),
    path("manager/newAgent/", views.SignUpView.as_view(), name="newAgent"),
    path("manager/newOffice/", views.CreateOfficeView.as_view(), name="newOffice"),
    path("manager/offices/", views.ListOffices.as_view(), name="listOffices"),
    path("manager/agents/", views.ListAgents.as_view(), name="listAgents"),
    path('increment/', views.increment_counter, name='increment_counter'),
    # api section 
    path('api/status/', views_api.status, name='apiStatus'),
    path('api/windows/<int:number_window>/assign-agent/', views_api.assign_agent_to_window, name='apiWindowAssignAgent'),
]
