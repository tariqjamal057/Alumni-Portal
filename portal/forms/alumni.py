from django import forms
from django.forms import ModelForm

from portal.models import Post


class Help_Desk_Form(ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "post_type"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "enter title", "class": "form-control", "id": "title"}
            ),
            "post_type": forms.Select(attrs={"class": "form-control", "id": "post_type"}),
        }
