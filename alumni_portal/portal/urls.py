from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('login.html', views.login, name="login"),
    path('Dashboard.html',views.loginredirect, name="loginredirect"),
    path('index.html',views.dashtoindex,name = "dashtoindex"),
    path('blog-archive.html',views.dashtobarchive,name="dashtobarchive"),
    path('blog-single.html',views.dashtobsingle,name = "dashtobsingle"),
    path('contact.html',views.dashtocontact,name ="dashtocontact"),
    path('course-detail.html',views.dashtocourse,name="dashtocourse"),
    path('gallery.html',views.gallery, name = 'gallery'),
    path('404.html',views.p404page,name = "p404page"),
]