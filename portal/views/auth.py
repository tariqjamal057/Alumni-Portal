from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import (
    PasswordResetCompleteView as AuthPasswordResetCompleteView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetDoneView as AuthPasswordResetDoneView
from django.contrib.auth.views import PasswordResetView as AuthPasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.generic.edit import CreateView

from alumni_portal import settings
from portal.forms.auth import PasswordResetForm, UserSignUpForm


class LoginView(AuthLoginView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")


class SignUpView(CreateView):
    form_class = UserSignUpForm
    template_name = "auth/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)


class PasswordResetView(AuthPasswordResetView):
    form_class = PasswordResetForm
    template_name = "auth/password_reset.html"
    from_email = settings.EMAIL_ADMIN
    email_template_name = "auth/emails/password_reset_email.html"
    html_email_template_name = "auth/emails/password_reset_email.html"


class PasswordResetDoneView(AuthPasswordResetDoneView):
    template_name = "auth/password_reset_done.html"


class PasswordResetConfirmView(AuthPasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = "auth/password_reset_confirm.html"
    email_template_name = "auth/emails/password_complete_successful.html"

    def form_valid(self, form: Form) -> HttpResponse:
        """
        Validates a form and sends a password reset complete mail if the form is valid.

        Parameters:
            form (Form): The form to be validated.

        Returns:
            HttpResponse: The response with the form data if the form is valid.
        """

        uidb64 = self.kwargs.get("uidb64")
        user = self.get_user(uidb64)
        subject = "Password Reset Successfully"
        to_email = None
        current_site = get_current_site(self.request)
        context = {
            "user": user,
            "domain": current_site.domain,
            "protocol": "http" if self.request.is_secure() else "https",
        }

        if user:
            to_email = user.email  # Retrieve the user's email
            html_content = render_to_string(self.email_template_name, context)
            email = EmailMultiAlternatives(
                subject=subject,
                body=strip_tags(html_content),  # Use the text version of the email (stripped HTML)
                from_email=settings.EMAIL_ADMIN,
                to=[to_email],
            )
            # Attach the HTML content to the email
            email.attach_alternative(html_content, "text/html")
            email.send()

        return super().form_valid(form)


class PasswordResetCompleteView(AuthPasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"
