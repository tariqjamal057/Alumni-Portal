from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('templates/login.html', views.login, name="login"),
    path('templates/Dashboard.html',views.loginredirect, name="loginredirect"),
    path('templates/index.html',views.dashtoindex,name = "dashtoindex"),
    path('templates/blog-archive.html',views.dashtobarchive,name="dashtobarchive")
]