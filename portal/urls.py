from unicodedata import name
from urllib import request

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path
from django.urls import re_path as url

from portal.views import alumni, auth, dasboard, public

from . import view

urlpatterns = [
    # path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    # path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    # path(
    #     "password_reset_confirm/<uidb64>/<token>",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path("password_reset_done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path(
    #     "password_reset_complete/",
    #     PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
    url(r"^password/$", view.change_password, name="change_password"),
    path("home/", view.home, name="home"),
    # path("dashboard/", view.dashboard, name="dashboard"),
    path("dashboard/faculty/", view.faculty, name="faculty-dashboard"),
    # path("dashboard/alumini", view.alumini, name="alumini-dashboard"),
    path("dashboard/student", view.student, name="student-dashboard"),
    path("blog-archive/", view.blog, name="blog-archive"),
    path("blog-single/", view.blog_single, name="blog-single"),
    # path("contact/", view.contact, name="contact"),
    path("course-detail/", view.course, name="course"),
    path("gallery1/", view.gallery, name="gallery"),
    # path("404/", view.page404, name="page404"),
    path("faculty_post_search/", view.faculty_post_search, name="faculty_post_search"),
    path("create-finance-request/", view.create_Finance_Post, name="create-finance-request"),
    path("update-finance-post/<int:pk>", view.update_Finance_Post, name="update-finance-post"),
    path("delete-finance-post/", view.delete_Finance_Post, name="delete-finance-post"),
    path("view_datails/<int:pk>", view.view_detail_page, name="request_details"),
    path("finance_request_chat/<int:pk>", view.finance_request_chat, name="finance_request_chat"),
    path(
        "get_finance_request_messages/",
        view.get_interest_message,
        name="get_finance_request_messages",
    ),
    path("faculty_chat/", view.faculty_addchat, name="faculty_chat"),
    path("get_interest/", view.get_interest, name="get_interest"),
    path("add_amount/", view.add_finance_amount, name="add_amount"),
    path("add_sponser/", view.add_sponser, name="add_sponser"),
    path("finance_requests/", view.finance_request_page, name="finance_request"),
    path(
        "request_detail_page/<int:pk>",
        view.finance_request_detail_page,
        name="request_detail_page",
    ),
    path(
        "alumni_as_sponser_chat/<int:pk>",
        view.alumni_as_sponser_chat,
        name="alumni_as_sponser_chat",
    ),
    path("alumni_response/", view.alumini_message, name="alumini_message"),
    path("alumni_post_search/", view.alumni_post_search, name="alumni_post_search"),
    # path("create-help-desk-post/", view.create_help_desk_post, name="create-help-desk-post"),
    # path(
    #     "update_help_desk_post/<int:pk>/",
    #     view.update_help_desk_post,
    #     name="update_help_desk_post",
    # ),
    # path(
    #     "help_desk_post_detail/<int:pk>", view.help_desk_post_detail, name="help_desk_post_detail"
    # ),
    # path("delete-help-desk-post/", view.delete_help_desk_post, name="delete-help-desk-post"),
    # path("help_desk_post_chat/<int:pk>", view.help_desk_post_chat, name="help_desk_post_chat"),
    path(
        "get_help_desk_chat_header/",
        view.get_help_desk_chat_header,
        name="get_help_desk_chat_header",
    ),
    path(
        "help_desk_interest_message/",
        view.help_desk_interest_message,
        name="help_desk_interest_message",
    ),
    path("alumni_addchat/", view.alumni_addchat, name="alumni_addchat"),
    path("help_desk_post/", view.help_desk_page, name="help_desk_post"),
    path(
        "help_desk_detail_page/<int:pk>", view.help_desk_detail_page, name="help_desk_detail_page"
    ),
    path("help_desk_chat/<int:pk>", view.help_desk_chat, name="help_desk_chat"),
    path("help_desk_users_message/", view.help_desk_users_message, name="help_desk_users_message"),
    path("student_post_search/", view.student_post_search, name="student_post_search"),
    path("create_mentor_help_post/", view.create_mentor_help_post, name="create_mentor_help_post"),
    path(
        "update_mentor_help_post/<int:pk>/",
        view.update_mentor_help_post,
        name="update_mentor_help_post",
    ),
    path(
        "mentor_help_post_detail/<int:pk>",
        view.mentor_help_post_detail,
        name="mentor_help_post_detail",
    ),
    path("delete_mentor_help_post/", view.delete_mentor_help_post, name="delete_mentor_help_post"),
    path(
        "mentor_help_post_chat/<int:pk>", view.mentor_help_post_chat, name="mentor_help_post_chat"
    ),
    path(
        "get_mentor_help_chat_header/",
        view.get_mentor_help_chat_header,
        name="get_mentor_help_chat_header",
    ),
    path(
        "mentor_help_interest_message/",
        view.mentor_help_interest_message,
        name="mentor_help_interest_message",
    ),
    path("mentor_addchat/", view.mentor_addchat, name="mentor_addchat"),
    path("mentor_help_page/", view.mentor_help_page, name="mentor_help_page"),
    path(
        "mentor_help_detail_page/<int:pk>",
        view.mentor_help_detail_page,
        name="mentor_help_detail_page",
    ),
    path("mentor_help_chat/<int:pk>", view.mentor_help_chat, name="mentor_help_chat"),
    path(
        "mentor_help_users_message/",
        view.mentor_help_users_message,
        name="mentor_help_users_message",
    ),
]

urlpatterns += [
    path("login/", auth.LoginView.as_view(), name="login"),
    path("signup/", auth.SignUpView.as_view(), name="signup"),
    path("password_reset/", auth.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password_reset_done/", auth.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "password_reset_complete/",
        auth.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

urlpatterns += [
    path("", public.Home.as_view(), name="home"),
    path("about", public.About.as_view(), name="about"),
    path("gallery", public.Gallery.as_view(), name="gallery"),
    path("contact", public.Contact.as_view(), name="contact"),
    path("404", public.Page404.as_view(), name="page404"),
]

urlpatterns += [
    path("dashboard", dasboard.DashboardView.as_view(), name="dashboard"),
]

urlpatterns += [
    path("dashboard/alumni", alumni.AlumniDashboard.as_view(), name="dashboard.alumni"),
    path(
        "dashboard/alumni/help-desk/create",
        alumni.CreateHelpDeskPost.as_view(),
        name="alumni.help_desk.create",
    ),
    path(
        "dashboard/alumni/help-desk/update/<int:pk>",
        alumni.UpdateHelpDeskPost.as_view(),
        name="alumni.help_desk.update",
    ),
    path(
        "dashboard/alumni/help-desk/detail/<int:pk>",
        alumni.HelpDeskPostDetailView.as_view(),
        name="alumni.help_desk.detail",
    ),
    path(
        "dashboard/alumni/help-desk/delete/<int:pk>",
        alumni.DeleteHelpDeskPostView.as_view(),
        name="alumni.help_desk.delete",
    ),
]
