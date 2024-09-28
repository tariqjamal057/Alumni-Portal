from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from portal.models import User

UserModel = get_user_model()


class UserSignUpForm(UserCreationForm):
    """
    A form for user sign-up, inheriting from UserCreationForm.

    This form includes an email field for user registration.
    """

    email = UserModel._meta.get_field(UserModel.USERNAME_FIELD)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)


class PasswordResetForm(PasswordResetForm):
    """"""

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()
