from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView , LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('', LogoutView.as_view(next_page="login"), name="logout"),
    path('', views.Home,name="home"),
    path('dashboard/',views.Dashboard, name="dashboard"),
    path('blog-archive/',views.dashtobarchive,name="dashtobarchive"),
    path('blog-single/',views.dashtobsingle,name = "dashtobsingle"),
    path('contact/',views.Contact,name ="contact"),
    path('course-detail/',views.dashtocourse,name="dashtocourse"),
    path('gallery/',views.Gallery, name = 'gallery'),
    path('404/',views.Page404,name = "page404"),
    path('create-finance-post/',views.Create_Finance_Post,name = "create-finance-post"),
]