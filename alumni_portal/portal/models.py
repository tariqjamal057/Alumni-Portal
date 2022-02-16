from operator import truediv
from tkinter import CASCADE
from turtle import title
from unicodedata import category
from django.db import models
# from django.contrib.auth.models import 
# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin 
from ckeditor.fields import RichTextField

gender_options = (('','Choose Gender'),('M','Male'),('F','Female'))


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
    name =models.CharField(max_length=30)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Batch(models.Model):
    
    entry_year = models.IntegerField()
    passed_out = models.IntegerField()
    def __str__(self):
        return self.entry_year + "-" + self.passed_out


class Department(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.short_name

class User(AbstractBaseUser , PermissionsMixin):
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'),unique=True )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.CharField(choices=gender_options,max_length=1,blank=True)
    dob = models.DateField(blank=True,null=True)    
    mobile_no=models.CharField(max_length=10,blank=True,null=True)
    profile_photo=models.ImageField(blank=True,null=True,upload_to="profile_picture")
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,blank=True,null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    location = models.CharField(max_length=100,null=True,blank=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE,null=True,blank=True)
    current_address=models.TextField(blank=True,null=True)
    permanent_address = models.TextField(blank=True,null=True)
    registered_on=models.DateField(auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False) 
    is_staff=models.BooleanField(default=False)     
    groups=models.ManyToManyField(Group)
     
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    

    @property
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


    def __str__(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        if self.first_name and not self.last_name:
            return self.first_name        
        elif self.last_name and not self.first_name:
            return self.name
        elif not self.first_name and not self.last_name:
            return self.username
        else:
            return self.username

class Post_Education_Detail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    degree = models.CharField(max_length=256)
    institute_or_university = models.CharField(max_length=100)
    currently_pursing_this = models.BooleanField(default=False)
    from_date = models.DateField()
    to_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.user.first_name + self.degree


class Experience_Detail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    organization = models.CharField(max_length=256)
    currently_working_here = models.BooleanField(default=False)
    from_date = models.DateField()
    to_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.user.first_name + self.designation


post_type_options = (
    ('O','Opportunity') , ('S','Seeking Job') , ('I','Internship')
)
class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    timeStamp = models.DateTimeField(auto_now_add=True)
    postType = models.CharField(choices=post_type_options,max_length=1,blank=True)
    deadLine = models.DateField(null=True)

class Post_Response(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    user = models.ForeignKey(Post , on_delete=models.CASCADE)

class Response_Message(models.Model):
    user = models.ForeignKey(Post , on_delete=models.CASCADE)
    postResponse = models.ForeignKey(Post_Response , on_delete= models.CASCADE)
    message = models.TextField()
    timeStamp = models.DateTimeField()


categories_type = (
    ('D','Web Developement') , ('G','Graphic Design') , ('AI','Artificial Intelegence') , ('DS','Data Science') , ('M','Math') , ('P','Physics') , ('C','Chemistry') , ('P','Physics') , ('E','English')
)
class SPost(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    timeStamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices= categories_type,max_length=2,null=True)

class Mentor_Post_Response(models.Model):
    post = models.ForeignKey(SPost , on_delete=models.CASCADE)
    user = models.ForeignKey(SPost , on_delete=models.CASCADE)

class Mentor_Response_Message(models.Model):
    user = models.ForeignKey(SPost , on_delete=models.CASCADE)
    postResponse = models.ForeignKey(Mentor_Post_Response , on_delete= models.CASCADE)
    message = models.TextField()
    timeStamp = models.DateTimeField()

type_of_sponsership = (
    ('E','Education Sponsership') , ('S','Culturals Sponsership') , ('I','InKind Sponsership') , ('P','Promotional Sponsership')
)
class Student_Support(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    desc = models.TextField(blank=True,null=True)
    typeOfSponser = models.CharField(choices=type_of_sponsership , max_length=1)

    # postedby

    
# class Sponser(models.Model):


