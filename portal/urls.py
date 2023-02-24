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
    path('blog-archive/',views.blog,name="blog-archive"),
    path('blog-single/',views.blog_single,name = "blog-single"),
    path('contact/',views.contact,name ="contact"),
    path('course-detail/',views.course,name="course"),
    path('gallery/',views.gallery, name = 'gallery'),
    path('404/',views.page404,name = "page404"),

    path('faculty_post_search/',views.faculty_post_search,name = "faculty_post_search"),
    path('create-finance-request/',views.create_Finance_Post,name = "create-finance-request"),
    path('update-finance-post/<int:pk>',views.update_Finance_Post,name = "update-finance-post"),
    path('delete-finance-post/',views.delete_Finance_Post,name = "delete-finance-post"),
    path('view_datails/<int:pk>',views.view_detail_page , name="request_details"),
    path('finance_request_chat/<int:pk>',views.finance_request_chat,name = "finance_request_chat"),
    path('get_finance_request_messages/',views.get_interest_message,name="get_finance_request_messages"),
    path('faculty_chat/',views.faculty_addchat,name="faculty_chat"),
    path('get_interest/',views.get_interest,name='get_interest'),
    path('add_amount/',views.add_finance_amount,name = "add_amount"),
    path('add_sponser/',views.add_sponser,name = "add_sponser"),

    path('finance_requests/',views.finance_request_page,name="finance_request"),
    path('request_detail_page/<int:pk>',views.finance_request_detail_page,name="request_detail_page"),
    path('alumni_as_sponser_chat/<int:pk>',views.alumni_as_sponser_chat,name="alumni_as_sponser_chat"),
    path('alumni_response/',views.alumini_message,name="alumini_message"),



    path('alumni_post_search/',views.alumni_post_search,name = "alumni_post_search"),
    path('create-help-desk-post/',views.create_help_desk_post,name = "create-help-desk-post"),
    path('update_help_desk_post/<int:pk>/',views.update_help_desk_post, name='update_help_desk_post'),
    path('help_desk_post_detail/<int:pk>',views.help_desk_post_detail , name="help_desk_post_detail"),
    path('delete-help-desk-post/',views.delete_help_desk_post,name = "delete-help-desk-post"),
    path('help_desk_post_chat/<int:pk>',views.help_desk_post_chat,name = "help_desk_post_chat"),
    path('get_help_desk_chat_header/',views.get_help_desk_chat_header,name='get_help_desk_chat_header'),
    path('help_desk_interest_message/',views.help_desk_interest_message,name="help_desk_interest_message"),
    path('alumni_addchat/',views.alumni_addchat,name="alumni_addchat"),

    path('help_desk_post/',views.help_desk_page,name="help_desk_post"),
    path('help_desk_detail_page/<int:pk>',views.help_desk_detail_page,name="help_desk_detail_page"),
    path('help_desk_chat/<int:pk>',views.help_desk_chat,name="help_desk_chat"),
    path('help_desk_users_message/',views.help_desk_users_message,name="help_desk_users_message"),



    path('student_post_search/',views.student_post_search,name = "student_post_search"),
    path('create_mentor_help_post/',views.create_mentor_help_post,name = "create_mentor_help_post"),
    path('update_mentor_help_post/<int:pk>/',views.update_mentor_help_post, name='update_mentor_help_post'),
    path('mentor_help_post_detail/<int:pk>',views.mentor_help_post_detail , name="mentor_help_post_detail"),
    path('delete_mentor_help_post/',views.delete_mentor_help_post,name = "delete_mentor_help_post"),
    path('mentor_help_post_chat/<int:pk>',views.mentor_help_post_chat,name = "mentor_help_post_chat"),
    path('get_mentor_help_chat_header/',views.get_mentor_help_chat_header,name='get_mentor_help_chat_header'),
    path('mentor_help_interest_message/',views.mentor_help_interest_message,name="mentor_help_interest_message"),
    path('mentor_addchat/',views.mentor_addchat,name="mentor_addchat"),

    path('mentor_help_page/',views.mentor_help_page,name="mentor_help_page"),
    path('mentor_help_detail_page/<int:pk>',views.mentor_help_detail_page,name="mentor_help_detail_page"),
    path('mentor_help_chat/<int:pk>',views.mentor_help_chat,name="mentor_help_chat"),
    path('mentor_help_users_message/',views.mentor_help_users_message,name="mentor_help_users_message"),

]