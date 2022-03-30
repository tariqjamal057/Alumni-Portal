
from django.forms import ModelForm
from .models import Filter_Finance, Finance_request, Mark

class FinanceHelpForm(ModelForm):
    class Meta:
        model = Finance_request
        fields = ['title','image','student_name','description','amount','marks','achievements','deadline']

class Filterfinance(ModelForm):
    class Meta:
        model = Filter_Finance
        fields = ['date','amount']

class MarkForm(ModelForm):
    class Meta:
        model = Mark
        fields = ['exam','percentage_or_cgpa']