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
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager

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



# # Added codes 

# class Content(models.Model):
#     title = models.CharField(max_length=200 , blank=True ,null=True)
#     content = models.CharField(max_length=1000)

# class Req(models.Model):
#     title = models.CharField(max_length=200 , blank=True ,null=True)
#     content = models.CharField(max_length=200)

# class Post(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     photo = models.ImageField(blank=True,null=True,upload_to="post_image")
#     title = models.CharField(max_length=200)
#     timestamp = models.DateTimeField(auto_now=True)
#     content = models.ForeignKey(Content,on_delete=models.CASCADE)
#     requirement = models.ForeignKey(Req , blank=True ,null=True  ,on_delete=models.CASCADE)
#     category = models.CharField(max_length=100)


# class Chat(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     postname = models.ForeignKey(Post,on_delete=models.CASCADE)
#     content = models.CharField(max_length=1000)
#     timestamp = models.DateTimeField(auto_now = True)


class chat(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name.User.username+ self.date

class Content(models.Model):
    title = models.CharField(max_length=200 , blank=True ,null=True)
    content = models.CharField(max_length=1000)

class Post(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True) 
    description = models.ForeignKey(Content, on_delete=models.CASCADE)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE)
    createdon = models.DateTimeField(auto_now_add=True)
    categories = models.CharField(max_length=100, choices=categories_options,default='select_type')
    archives = models.CharField(max_length=100, choices=archives_options,default='select_type')
    photos = models.ImageField(upload_to='photo')
    tags = models.CharField(max_length=100, choices=tags_options,default='select_type')
    
    slug = models.SlugField(unique=True, max_length=255)


    def get_absolute_url(self):
        return reverse('portal_post_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created_on']

        def _unicode_(self):
            return self.title


    def __str__(self):
        return self.title +self.createdby
    


class alumniasmentor(models.Model):
    title = models.ForeignKey(Post, on_delete=models.CASCADE)
    createdby = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Post, on_delete=models.CASCADE)
    archives = models.ForeignKey(Post, on_delete=models.CASCADE)
    tags = models.ForeignKey(Post, on_delete=models.CASCADE)
    #share = 
    commit = models.BooleanField(default=False)
    photos = models.ForeignKey(Post, on_delete=models.CASCADE)
    createdon = models.ForeignKey(Post, on_delete=models.CASCADE)

class comments(models.Model):
    name = models.CharField(max_length=42, blank=True, null=True)
    createdon = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Sponsers_Details(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    dateTime = models.DateTimeField()
    workOrganization = models.CharField(max_length=100)
    amount = models.IntegerField()
    message = models.TextField()
    phoneNumber = models.IntegerField(max_length=10)
    email = models.EmailField(max_length=250)


class student_detail(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    fatherOccupation = models.CharField(max_length=50)
    motherOccupation = models.CharField(max_length=50)
    familyAnnual_income = models.CharField()
    sslcPercentage = models.CharField()
    hscPercentage = models.CharField()
    cgpa = models.CharField()
    totalFee = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10,decimal_places=2)


        
