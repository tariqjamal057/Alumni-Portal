from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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
