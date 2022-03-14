
from django.forms import ModelForm
from .models import Finance_request, Mark

class FinanceHelpForm(ModelForm):
    class Meta:
        model = Finance_request
        fields = ['title','image','student_name','description','amount','marks','achievements','deadline']
class MarkForm(ModelForm):
    class Meta:
        model = Mark
        fields = ['exam','percentage_or_cgpa']