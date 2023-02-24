import datetime
from django import forms
from django.forms import ModelForm
from .models import Finance_request, Post, Tech_Help_Post , Featured_Sponser

class FinanceHelpForm(ModelForm):
    class Meta:
        model = Finance_request
        fields = ['title','image','name','department','year', 'description','achievements','other_performance']
        widgets={
            'title':forms.TextInput(attrs={'placeholder':'Enter Title','class':'form-control','id':'title'}),
            'image':forms.FileInput(attrs={'class':'form-control','id':'image'}),
            'name':forms.TextInput(attrs={'placeholder':'Enter Name Of The Student','class':'form-control','id':'name'}),
            'department': forms.Select(attrs={'class':'form-control','id':'department'}),
            'year': forms.Select(attrs={'class':'form-control','id':'year'}),
            'description':forms.Textarea(attrs={'placeholder':'Enter Description','class':'form-control','rows':'4','id':'description'}),
            'achievements':forms.Textarea(attrs={'placeholder':'Enter Achievements Of the Student','class':'form-control','rows':'4','id':'achievements'}),
            'other_performance':forms.Textarea(attrs={'placeholder':'Enter Extra-Curricular Activity Of The Student','class':'form-control','rows':'4','id':'other-performance'})
        }


class Help_Desk_Form(ModelForm):
    content = forms.CharField(label='Content',widget=forms.Textarea(attrs={'class': 'ckeditor'}))
    class Meta:
        model = Post
        fields = ['title','content','post_type']
        widgets = {
            'title':forms.TextInput(attrs={'placeholder':'enter title','class':'form-control','id':'title'}),
            'post_type':forms.Select(attrs={'class':'form-control','id':'post_type'}),
        }

class MentorHelpForm(ModelForm):
    content = forms.CharField(label='Content',widget=forms.Textarea(attrs={'class': 'ckeditor'}))
    class Meta:
        model = Tech_Help_Post
        fields = ['title','stack','content']
        widgets = {
            'title':forms.TextInput(attrs={'placeholder':'enter title','class':'form-control','id':'title'}),
            'stack':forms.TextInput(attrs={'placeholder':'enter stacks','class':'form-control','id':'stack'}),
        }