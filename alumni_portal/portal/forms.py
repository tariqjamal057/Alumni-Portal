
from dataclasses import field
import datetime
from email.mime import image
from django import forms
from django.forms import ModelForm
from .models import Finance_request, Post, Tech_Help_Post , Featured_Sponser

class FinanceHelpForm(ModelForm):
    class Meta:
        model = Finance_request
        fields = ['title','image','name','department','year', 'description','achievements','other_performance']
        widgets={
            'title':forms.TextInput(attrs={'placeholder':'enter title','class':'form-control','id':'title'}),
            'image':forms.FileInput(attrs={'class':'form-control','id':'image'}),
            'name':forms.TextInput(attrs={'placeholder':'enter name of the student','class':'form-control','id':'name'}),
            'department': forms.Select(attrs={'class':'form-control','id':'department'}),
            'year': forms.Select(attrs={'class':'form-control','id':'year'}),
            'description':forms.Textarea(attrs={'placeholder':'enter description','class':'form-control','rows':'4','id':'description'}),
            'achievements':forms.Textarea(attrs={'placeholder':'enter achievements of the student','class':'form-control','rows':'4','id':'achievements'}),
            'other_performance':forms.Textarea(attrs={'placeholder':'enter extra-curricular activity of the student','class':'form-control','rows':'4','id':'other-performance'})
        }


class Help_Desk_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','post_type']

class MentorHelpForm(ModelForm):
    class Meta:
        model = Tech_Help_Post
        fields = ['title','stack','content']


