from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

from portal.forms import FinanceHelpForm

# from portal.models import allowed_user

# Create your views here.
def Home(request):
    return render(request,'index.html')
    
def login(request):
    return render(request , 'accounts/login.html')

@login_required(login_url='login')
# @allowed_user(allowed_roles=['staff','alumini'])
def Dashboard(request):
    return render(request,'Dashboard.html')

@login_required(login_url='login')
def dashtobarchive (request):
    return render (request,'blog-archive.html')

@login_required(login_url='login')
def dashtobsingle (request):
    return render (request,'blog-single.html')



def Contact(request):
    return render (request,'contact.html')

def dashtocourse (request):
    return render (request,'course-detail.html')

def Gallery(request):
    return render (request,'gallery.html')

def Page404(request):
    return render (request,'404.html')

def Create_Finance_Post(request):
    form = FinanceHelpForm()
    if request.method == 'POST':
        form = FinanceHelpForm()
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form':form}
    return render (request,'Finance/create.html',context)