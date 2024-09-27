from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from alumni_portal import settings
from portal.forms.auth import UserSignUpForm


class LoginView(AuthLoginView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")


class SignUpView(CreateView):
    form_class = UserSignUpForm
    template_name = "auth/signup.html"
    success_url = reverse_lazy(settings.LOGIN_URL)
