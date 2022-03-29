# from operator import truediv
# from tkinter import CASCADE
# from turtle import title
# from unicodedata import category
from datetime import datetime
from django.db import models
# from django.contrib.auth.models import 
# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.forms import CharField, DateField, DateTimeField
from django.http import HttpResponse
# from django.core.exceptions import ValidationError
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

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

class UserManager(BaseUserManager):

    def create_superuser(self,email,username,password,**other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('SuperUser must be assingned as Staff status to true'))

        return self.create_user(email , username , password , **other_fields)

        

    def create_user(self,email,username,password,**other_fields):
        email = self.normalize_email(email)
        user = self.model(email = email , username = username , **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser , PermissionsMixin):
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'),unique=True )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.CharField(choices=gender_options,max_length=1,blank=True)
    dob = models.DateField(blank=True,null=True)    
    mobile_no=models.CharField(max_length=10,blank=True,null=True)
    profile_photo=models.ImageField(blank=True,null=True,upload_to="profile_picture")
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,blank=True,null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
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
    REQUIRED_FIELDS = ['username']

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

class PostEducationDetail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    degree = models.CharField(max_length=256)
    institute_or_university = models.CharField(max_length=100)
    currently_pursing_this = models.BooleanField(default=False)
    from_date = models.DateField()
    to_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.user.first_name + self.degree


class ExperienceDetail(models.Model):
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
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user',null=True, blank=True)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    timeStamp = models.DateTimeField(auto_now_add=True)
    postType = models.CharField(choices=post_type_options,max_length=1,blank=True)
    deadLine = models.DateField(null=True,blank=True)
    posted_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name='postedby', null=True, blank=True)

class PostResponse(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='helpdeskpost')
    user = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='helpdeskuser')

class ResponseMessage(models.Model):
    user = models.ForeignKey(Post , on_delete=models.CASCADE)
    postResponse = models.ForeignKey(PostResponse , on_delete= models.CASCADE)
    message = models.TextField()
    timeStamp = models.DateTimeField()


categories_type = (
    ('D','Web Developement') , ('G','Graphic Design') , ('AI','Artificial Intelegence') , ('DS','Data Science') , ('M','Math') , ('P','Physics') , ('C','Chemistry') , ('P','Physics') , ('E','English') , ('EC','Electronics and Communication')
)
class Tech_Help_Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='techhelpuser',null=True, blank=True)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    timeStamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices= categories_type,max_length=2,null=True)
    deadLine = models.DateField(null=True,blank=True)
    posted_by = models.ForeignKey(User , on_delete=models.CASCADE  ,related_name='alumininame', null=True, blank=True)

class Tech_Help_PostResponse(models.Model):
    post = models.ForeignKey(Tech_Help_Post , on_delete=models.CASCADE , related_name='studentpost')
    user = models.ForeignKey(Tech_Help_Post , on_delete=models.CASCADE , related_name='student')

class Tech_Help_ResponseMessage(models.Model):
    user = models.ForeignKey(Tech_Help_Post , on_delete=models.CASCADE)
    postResponse = models.ForeignKey(Tech_Help_PostResponse , on_delete= models.CASCADE)
    message = models.TextField()
    timeStamp = models.DateTimeField()

mode_of_payment = (
    ('O','Online Banking') , ('N','Net Banking') , ('U','UPI') , ('C','Credit/Debit card'), ('A','Cash'))

class Mark(models.Model):
    exam = models.CharField(max_length=50)
    percentage_or_cgpa =  models.DecimalField(max_digits=4,decimal_places=1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.exam
    
class Acheivement(models.Model):
    name = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Finance_request(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to ='student_images/')
    student_name = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.IntegerField()
    marks = models.ForeignKey(Mark,on_delete=models.CASCADE , related_name='student_marks')
    achievements = models.ManyToManyField(Acheivement ,related_name='student_achievement')
    deadline = models.DateField(default=datetime.now)
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.student_name

class Finance_request_Post_Response(models.Model):
    post = models.ForeignKey(Finance_request , on_delete=models.CASCADE , related_name='helpdeskpost')
    user = models.ForeignKey(Finance_request , on_delete=models.CASCADE , related_name='helpdeskuser')

class Finance_request_Response_Message(models.Model):
    postResponse = models.ForeignKey(Finance_request_Post_Response , on_delete= models.CASCADE , related_name='post_response')
    message_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="from_user")
    message_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name="to_user")
    message = models.TextField()
    date = models.DateTimeField()

class Finance(models.Model):
    studentname = models.ForeignKey(Finance_request ,on_delete=models.CASCADE , related_name='studentname')
    studentdetails = models.ForeignKey(Finance_request, on_delete=models.CASCADE , related_name='details')
    timestamp = models.DateField(auto_now_add=True)
    modeofpayment = models.CharField(choices=mode_of_payment , max_length=1)

    def __str__(self):
        return self.studentname.student_name
