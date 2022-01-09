from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


typeof_event = (
    ('select' , 'Select'),
    ('Dept' , 'Department Event'),
    ('college', 'College Event'),
)

dept = (
    ('select' , 'Select Department'),
    ('it' , 'Information Technology'),
    ('cse', 'Computer Science and Engineering'),
    ('aids' , 'Artificial Intelegence and Data Science'),
    ('ece', 'Electronics and Communication Engineering'),
    ('eee', 'ELectrical and Electronic Engineering'),
    ('mech', 'Mechanical Engineering'),
)
modeof_event = (
    ('select_mode','Select the mode of event'),
    ('intercollege-event','Inter college Event'),
    ('intracollege-event','Intra college Event'),
)
listof_event = (
    ('select_event','Select event'),
    ('symposium','Symposium'),
    ('workshop','Workshop'),
    ('hackathon','Hackathon'),
)
eventmode = (
    ('select_type','Select the type of event'),
    ('both','Both'),
    ('technical','Technical'),
    ('non-technical','Non Technical'),
)

select_degree = (
    ('s' , 'Select'),
    ('btech', 'Bachelor of Technology'),
    ('be', 'Bachelor of Engineering'),
)

select_specialization = (
    ('s' , 'Seelct'),
    ('it', 'Information Technology'),
    ('cse', 'Computer Science Engineering'),
    ('aids', 'Artificial Inteligence and Data Science'),
    ('ece', 'Electronics and Communication Engineering'),
    ('eee', 'ELectrical and Electronic Engineering'),
    ('mech', 'Mechanical Engineering'),
    )
amp = (
    ('select' , 'Select Amplifer'),
    ('120hz' , '120 Hz Amplifier'),
    ('90hz' , '90 Hz Amplifier'),
)

no_mic = (
    ('s' , 'Select'),
    ('0' , 'Null'),
    ('1' , '1 Mic'),
    ('2' , '2 Mic'),
    ('3' , '3 Mic'),
    ('4' , '4 Mic'),
)

no_speaker = (
    ('s' , 'Select'),
    ('0' , 'Null'),
    ('1' , '1 Speaker'),
    ('2' , '2 Speaker'),
    ('3' , '3 Speaker'),
    ('4' , '4 Speaker'),
)

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='speaker')
    designation = models.CharField(max_length=100)
    about = models.TextField()

    def __str__(self):
        return self.name


class Partner(models.Model):
    image = models.ImageField(upload_to='partner')
    
    

class Media(models.Model):
    gallery = models.FileField(upload_to='gallery')

class Theme(models.Model):
    event_name = models.CharField(max_length=100 , null=True)
    name = models.CharField(max_length=100 , null=True)
    image = models.ImageField(upload_to='theme' , null=True)
    desc = models.TextField(null=True)
  
    def __str__(self):
        return self.event_name

class Prize(models.Model):
    event_name = models.CharField(max_length=100 , null=True)
    prize_name = models.CharField(max_length=100 , null=True)
    image = models.ImageField(upload_to='prize')
    prize_money = models.PositiveBigIntegerField()
    prize_desc = models.TextField(null=True)
    def __str__(self):
        return self.event_name

class Faq(models.Model):
    event_name = models.CharField(max_length=100 , null=True)
    question = models.TextField(null=True)
    answer = models.TextField(null=True)
    def __str__(self):
        return self.event_name

class Feedback(models.Model):
    event_name = models.CharField(max_length=100 , null=True)
    question = models.TextField( null=True)
    def __str__(self):
        return self.event_name

class Event(models.Model):
    type_of_event = models.CharField(max_length=20, choices=typeof_event,default='select')
    department = models.CharField(max_length=50 , choices= dept , default='select')
    mode_of_event = models.CharField(max_length=50, choices=modeof_event,default='select_mode')
    event_mode = models.CharField(max_length=20, choices=eventmode, default='select_type')
    list_of_event = models.CharField(max_length=20, choices=listof_event,default='select_event')
    name = models.CharField(max_length=100)
    poster = models.FileField(upload_to='poster')
    description = models.TextField(null=True)
    venue = models.CharField(max_length=200)
    fees = models.DecimalField(max_digits=6 , decimal_places=2)
    coordinator = models.CharField(max_length=200 , null=True , blank=True)
    patron = models.CharField(max_length=200 , null=True , blank=True)
    cheif_patron = models.CharField(max_length=200 , null=True , blank=True)
    organizing_secretary = models.CharField(max_length=200 , null=True , blank=True)
    student_coordinator = models.CharField(max_length=200 , null=True , blank=True)
    co_coordinator = models.CharField(max_length=200 , null=True , blank=True)
    speaker = models.ManyToManyField('Speaker', related_name='speaker')
    participation_limit = models.PositiveIntegerField()
    amplifier = models.CharField(max_length=50, choices=amp , default='select')
    mic = models.CharField(max_length=50, choices=no_mic , default='s')
    speaker = models.CharField(max_length=50, choices=no_speaker , default='s')
    add_other_assesment = models.TextField(null=True , blank=True)
    budjet = models.BooleanField(null=True)
    budjet_money = models.DecimalField(max_digits=8 , decimal_places=2 , null=True , blank=True)
    event_start_at = models.DateTimeField()
    event_end_at = models.DateTimeField()
    registration_start_date = models.DateField()
    registration_end_date = models.DateField()
    registration_start_time = models.TimeField()
    registration_end_time = models.TimeField()
    main_event = models.BooleanField(null=True , blank=True)
    theme = models.ManyToManyField('Theme' , related_name='theme' , null=True , blank=True)
    prize = models.ManyToManyField('Prize' , related_name='prize' , null=True , blank=True)
    partner = models.ManyToManyField('Partner' , related_name='partner' , null=True , blank=True)
    gallery = models.ManyToManyField('Media' , related_name='media')
    faqs = models.ManyToManyField('Faq' , related_name='faqs' , null=True , blank=True)
    feedback = models.ManyToManyField('Feedback' , related_name='feedback' , null=True , blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User , related_name='user' , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=10 , primary_key=True)
    regno = models.CharField(max_length=20)
    degree = models.CharField(max_length=100 , choices=select_degree, default='s')
    specialization = models.CharField(max_length=100 , choices=select_specialization, default='s')
    phoneno = models.CharField(max_length=10)
    college = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.PositiveIntegerField()

    def __str__(self):
        return self.name
