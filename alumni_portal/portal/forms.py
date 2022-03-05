from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from .models import Finance_request

class FinanceHelpForm(ModelForm):
    class Meta:
        model = Finance_request
        fields = '__all__'