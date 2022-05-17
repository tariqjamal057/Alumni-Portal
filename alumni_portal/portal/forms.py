
from dataclasses import field
import datetime
from django import forms
from django.forms import ModelForm
from .models import Finance_request, Post, Tech_Help_Post , featured_Sponser

now_year = datetime.datetime.now().year
today_date=  datetime.datetime.now().day
today_month= datetime.datetime.now().month
now_date=datetime.date(now_year,today_month,today_date)

class FinanceHelpForm(ModelForm):
    class Meta:
        model = Finance_request
        fields = ['title','image','student_name','department','year', 'description','achievements','other_performance']

class addSponser(ModelForm):
    class Meta:
        model = featured_Sponser
        fields = ['student_name','user','amount']

class MentorHelpForm(ModelForm):
    deadline = forms.DateField(label="Date from", widget=forms.TextInput(attrs={'type': 'date', 'min': now_date}))
    class Meta:
        model = Tech_Help_Post
        fields = ['title','content','deadline']

class Help_Desk_Form(ModelForm):
    deadline = forms.DateField(label="Date from", widget=forms.TextInput(attrs={'type': 'date', 'min': now_date}))
    class Meta:
        model = Post
        fields = ['title','content','deadline']


