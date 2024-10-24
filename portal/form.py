import datetime

from django import forms
from django.forms import ModelForm

from .models import FinanceRequest, HelpDesk, TechHelpPost


class FinanceHelpForm(ModelForm):
    class Meta:
        model = FinanceRequest
        fields = [
            "title",
            "profile_img",
            "student",
            "year",
            "description",
            "achievements",
            "other_performance",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter Title", "class": "form-control", "id": "title"}
            ),
            # "image": forms.FileInput(attrs={"class": "form-control", "id": "image"}),
            # "name": forms.TextInput(
            #     attrs={
            #         "placeholder": "Enter Name Of The Student",
            #         "class": "form-control",
            #         "id": "name",
            #     }
            # ),
            "department": forms.Select(attrs={"class": "form-control", "id": "department"}),
            "year": forms.Select(attrs={"class": "form-control", "id": "year"}),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter Description",
                    "class": "form-control",
                    "rows": "4",
                    "id": "description",
                }
            ),
            "achievements": forms.Textarea(
                attrs={
                    "placeholder": "Enter Achievements Of the Student",
                    "class": "form-control",
                    "rows": "4",
                    "id": "achievements",
                }
            ),
            "other_performance": forms.Textarea(
                attrs={
                    "placeholder": "Enter Extra-Curricular Activity Of The Student",
                    "class": "form-control",
                    "rows": "4",
                    "id": "other-performance",
                }
            ),
        }


class Help_Desk_Form(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["post_type"].empty_label = "Select post type"

    class Meta:
        model = HelpDesk
        fields = ["title", "content", "post_type", "tags"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Post Title",
                }
            ),
            "post_type": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }


class MentorHelpForm(ModelForm):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"class": "ckeditor"}))

    class Meta:
        model = TechHelpPost
        fields = ["title", "stack", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "enter title", "class": "form-control", "id": "title"}
            ),
            "stack": forms.TextInput(
                attrs={"placeholder": "enter stacks", "class": "form-control", "id": "stack"}
            ),
        }
