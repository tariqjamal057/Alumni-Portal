from django.shortcuts import render
from. models import Finance_request

# Create your views here.
def student_Post(request):
	post = student_Post.objects.all()
	return render(request=request, template_name="studentpost.html", context={'studentpost':student_Post})