from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy


class UserManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        if other_fields.get("is_staff") is not True:
            raise ValueError(gettext_lazy("SuperUser must be assingned as Staff status to true"))

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user
