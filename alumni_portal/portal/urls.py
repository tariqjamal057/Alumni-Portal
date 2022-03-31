from unicodedata import name
from django.urls import path, re_path as url
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('', LogoutView.as_view(next_page="login"), name="logout")
    ,
    path('password_reset/', PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    url(r'^password/$', views.change_password, name='change_password')
    ,
    path('home/', views.home,name="home")
    ,
    path('dashboard/',views.dashboard, name="dashboard"),
    path('dashboard/faculty/',views.faculty, name="faculty-dashboard"),
    path('dashboard/alumini',views.alumini, name="alumini-dashboard"),
    path('dashboard/student',views.student, name="student-dashboard")
    ,
    path('blog-archive/',views.dashtobarchive,name="dashtobarchive"),
    path('blog-single/',views.dashtobsingle,name = "dashtobsingle"),
    path('contact/',views.contact,name ="contact"),
    path('course-detail/',views.dashtocourse,name="dashtocourse"),
    path('gallery/',views.gallery, name = 'gallery'),
    path('404/',views.page404,name = "page404")
    ,
    path('request/create-finance-post/',views.create_Finance_Post,name = "create-finance-post"),
    path('request/update-finance-post/',views.update_Finance_Post,name = "update-finance-post"),
    path('request/delete-finance-post/',views.delete_Finance_Post,name = "delete-finance-post"),
    path('finance_requests/',views.finance_request_page,name="finance_request")
    ,
    path('chat/',views.addResponse_Message,name="addchatmessage")
    ,
    path('request/create-mentor-help-post/',views.create_mentor_post,name = "create-mentor-help-post"),
    path('request/update-mentor-help-post/',views.update_mentor_post,name = "update-mentor-help-post"),
    path('request/delete-mentor-help-post/',views.delete_mentor_post,name = "delete-mentor-help-post"),
    path('mentor_help_posts/',views.alumini_as_mentor_page,name="mentor-help-post")
    ,
    path('load-more/',views.load_more,name='load-more')
    ,

]