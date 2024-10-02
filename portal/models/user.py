from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy

from core.constant import GenderEnum
from portal.managers.user import UserManager
from portal.models.base import BaseModel
from portal.models.college import Batch, Degree, DegreeSpecialization, Department


class Country(BaseModel):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="country_created_by"
    )
    updated_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="country_updated_by"
    )

    def __str__(self):
        return self.name


class State(BaseModel):
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="state_created_by"
    )
    updated_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="state_updated_by"
    )

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="district_created_by"
    )
    updated_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="district_updated_by"
    )

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30)
    email = models.EmailField(gettext_lazy("email address"), unique=True)
    first_name = models.CharField(gettext_lazy("first name"), max_length=30, null=True, blank=True)
    last_name = models.CharField(gettext_lazy("last name"), max_length=30, null=True, blank=True)
    gender = models.IntegerField(choices=GenderEnum.choices, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    mobile_no = models.CharField(max_length=10, null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to="profile_picture", null=True, blank=True, default="image/character.png"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    register_number = models.IntegerField(blank=True, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    permanent_address = models.CharField(max_length=100, null=True, blank=True)
    current_address = models.TextField(null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)
    registered_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="created_by"
    )
    is_active = models.BooleanField(gettext_lazy("active"), default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_created_by", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="user_updated_by"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = gettext_lazy("user")
        verbose_name_plural = gettext_lazy("users")

    @property
    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def send_verification(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.last_name and not self.first_name:
            return self.name
        elif not self.first_name and not self.last_name:
            return self.username
        else:
            return self.username


class PostEducationDetail(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_education_user")
    education_degree = models.ForeignKey(
        Degree, on_delete=models.CASCADE, related_name="post_education_degree"
    )
    speciazation = models.ForeignKey(DegreeSpecialization, on_delete=models.CASCADE)
    institute_or_university = models.CharField(max_length=100)
    currently_pursing = models.BooleanField(default=False)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="post_education_created_by"
    )
    updated_by = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="post_education_updated_by",
    )

    def __str__(self):
        return self.user.first_name + self.degree


class Experience(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_experience")
    designation = models.CharField(max_length=100)
    organization = models.CharField(max_length=256)
    currently_working_here = models.BooleanField(default=False)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="experience_detail_created_by"
    )
    updated_by = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="experience_detail_updated_by",
    )

    def __str__(self):
        return self.user.first_name + self.designation
