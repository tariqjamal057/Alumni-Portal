from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name='home'),
    # path('event/', views.event , name='event'),
]