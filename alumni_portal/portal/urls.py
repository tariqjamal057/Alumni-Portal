from unicodedata import name
from urllib import request
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

    path('create-finance-request/',views.create_Finance_Post,name = "create-finance-request"),
    path('request/update-finance-post/<int:pk>',views.update_Finance_Post,name = "update-finance-post"),
    path('request/delete-finance-post/',views.delete_Finance_Post,name = "delete-finance-post"),
    path('request/view_datails/<int:pk>',views.view_detail_page , name="request_details"),
    path('finance_requests/',views.finance_request_page,name="finance_request"),
    path('request_detail_page/<int:pk>',views.finance_request_detail_page,name="request_detail_page")
    ,

    path('finance_request_chat/<int:pk>',views.finance_request_chat,name = "finance_request_chat"),
    path('get_finance_request_messages/',views.get_interest_message,name="get_finance_request_messages"),
    path('faculty_chat/',views.faculty_addchat,name="faculty_chat"),
    path('get_interest/',views.get_interest,name='get_interest'),
    path('finance_response_interest/',views.get_finance_request_interest,name="finance_response_interest"),
    path('alumni_response/',views.alumini_message,name="alumini_message"),
    path('get_alumni_message/',views.get_alumni_message,name = "get_alumni_message"),
    path('add_amount/',views.add_finance_amount,name = "add_amount"),
    path('add_sponser/',views.add_sponser,name = "add_sponser")
    ,

    path('request/create_help_desk_post/',views.create_help_desk_post, name='create_help_desk_post'),
    path('request/update_help_desk_post/<int:pk>/',views.update_help_desk_post, name='update_help_desk_post'),
    path('request/delete_help_desk_post/',views.delete_post, name='delete_help_desk_post'),
    path('request/help_desk_detail_page/<int:pk>/',views.post_detail_page, name='help_desk_detail_page'),
    path('help_desk_page/',views.help_desk_page,name="help_desk_page"),
    path('post_detail/<int:pk>',views.post_detail,name="post_detail")
    ,

    path('get_user_interest/',views.get_user_interest,name = "get_user_interest"),
    path('user_response/',views.user_message,name="user_message"),
    path('get_user_message/',views.get_user_message,name = "get_user_message")
    ,

    path('request/create_mentor_help_post/',views.create_mentor_help_post, name='create_mentor_help_post'),
    path('request/update_mentor_help_post/<int:pk>/',views.update_mentor_help_post, name='update_mentor_help_post'),
    path('request/delete_mentor_help_post/',views.delete_mentor_help_post, name='delete_mentor_help_post'),
    path('request/mentor_help_detail_page/<int:pk>/',views.mentorhelp_post_detailpage, name='mentor_help_detail_page'),
    path('mentor_help_posts/',views.mentor_help_page,name="mentor_help_posts"),
    path('mentorhelp_post_details/<int:pk>',views.mentorhelp_post_details,name="mentorhelp_post_details")
    ,

    path('mentor_message/',views.mentor_message,name="mentor_message"),
    path('get_mentor_message/',views.get_mentor_message,name = "get_mentor_message")
    ,

]