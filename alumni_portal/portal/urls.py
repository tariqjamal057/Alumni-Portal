from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('templates/login.html', views.login, name="login"),
    path('templates/Dashboard.html',views.loginredirect, name="loginredirect"),
    path('templates/index.html',views.dashtoindex,name = "dashtoindex"),
    path('templates/blog-archive.html',views.dashtobarchive,name="dashtobarchive"),
    path('templates/blog-single.html',views.dashtobsingle,name = "dashtobsingle"),
    path('templates/contact.html',views.dashtocontact,name ="dashtocontact"),
    path('templates/course-detail.html',views.dashtocourse,name="dashtocourse"),
    path('templates/gallery.html',views.gallery, name = 'gallery'),
    path('templates/404.html',views.p404page,name = "p404page"),
]