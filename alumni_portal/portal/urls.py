from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('accounts/login.html', views.login, name="login"),
]