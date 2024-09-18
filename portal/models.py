# from operator import truediv
# from tkinter import CASCADE
# from turtle import title
# from unicodedata import category
from atexit import register
from datetime import datetime

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# from django.contrib.auth.models import
# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.forms import CharField, DateField, DateTimeField
from django.http import HttpResponse

# from django.core.exceptions import ValidationError
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.db.models import Q
from django.utils.translation import gettext_lazy as _

gender_options = (("", "Choose Gender"), ("M", "Male"), ("F", "Female"))


# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Batch(models.Model):

    entry_year = models.IntegerField()
    passed_out = models.IntegerField()

    def __str__(self):
        return str(self.entry_year) + "-" + str(self.passed_out)


class Department(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.short_name


class UserManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        if other_fields.get("is_staff") is not True:
            raise ValueError(_("SuperUser must be assingned as Staff status to true"))

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, null=True, blank=True)
    gender = models.CharField(choices=gender_options, max_length=1, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    mobile_no = models.CharField(max_length=10, null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to="profile_picture", null=True, blank=True, default="image/character.png"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    register_number = models.IntegerField(blank=True, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    current_address = models.TextField(null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)
    registered_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
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


class PostEducationDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=256)
    institute_or_university = models.CharField(max_length=100)
    currently_pursing = models.BooleanField(default=False)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)  ####

    def __str__(self):
        return self.user.first_name + self.degree


class ExperienceDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    organization = models.CharField(max_length=256)
    currently_working_here = models.BooleanField(default=False)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name + self.designation


year_option = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
)


class Finance_request(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="student_images")
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.CharField(choices=year_option, max_length=1)
    description = models.TextField()
    achievements = models.TextField(null=True)
    other_performance = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_interested_alumni(self):
        return Finance_request_Post_Response.objects.filter(post=self)


class Finance_request_Post_Response(models.Model):
    post = models.ForeignKey(
        Finance_request, on_delete=models.CASCADE, related_name="helpdeskpost"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="helpdeskuser")

    def get_alumni_msgs(self):
        return Finance_request_Response_Message.objects.filter(user=self.user)


class Finance_request_Response_Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_response = models.ForeignKey(Finance_request_Post_Response, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Featured_Sponser(models.Model):
    student_name = models.ForeignKey(
        Finance_request, on_delete=models.CASCADE, related_name="student_name", null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alumni")
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


post_type_options = (("O", "Opportunity"), ("S", "Seeking Job"), ("I", "Internship"))


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    post_type = models.CharField(choices=post_type_options, max_length=1)
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postedby")


class PostResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class ResponseMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_response = models.ForeignKey(PostResponse, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Tech_Help_Post(models.Model):
    title = models.CharField(max_length=200)
    stack = models.CharField(max_length=200)
    content = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="studentname")


class Tech_Help_PostResponse(models.Model):
    post = models.ForeignKey(Tech_Help_Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Tech_Help_ResponseMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_response = models.ForeignKey(Tech_Help_PostResponse, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Featured_Mentor(models.Model):
    post = models.ForeignKey(
        Tech_Help_Post, on_delete=models.CASCADE, related_name="mentor_post", null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mentor")
    date = models.DateTimeField(auto_now_add=True)
