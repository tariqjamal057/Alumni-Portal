from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.template.loader import render_to_string

from portal.forms import FinanceHelpForm, MarkForm
from portal.models import Finance_request

# from portal.models import allowed_user

# Create your views here.


def home(request):
    user = request.user
    context = {"user":user}
    return render(request,'index.html',context)
    
def login(request):
    return render(request , 'registration/login.html')

def is_student(user):
    return user.groups.filter(name='student').exists()

def is_alumini(user):
    return user.groups.filter(name='alumini').exists()

def is_faculty(user):
    return user.groups.filter(name='faculty').exists()

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {'form': form})

def dashboard(request):
    if is_faculty(request.user):
        return redirect('faculty-dashboard')
    elif is_alumini(request.user):
        return redirect('alumini-dashboard')
    elif is_student(request.user):
        return redirect('student-dashboard')
    else:
        return redirect('page404')

@login_required()
def faculty(request):
    form = FinanceHelpForm()
    # form1 = MarkForm()
    requests = Finance_request.objects.filter(posted_by = request.user).order_by('-id')

    context = {
        "requests" : requests,
        "form":form,
        # "form1":form1,
    }
    return render(request,'faculty/faculty-dashboard.html',context)

@login_required()
def alumini(request):
    return render(request,'alumini/alumini-dashboard.html')

@login_required()
def student(request):
    return render(request,'student/student-dashboard.html')

def dashtobarchive (request):
    return render (request,'blog-archive.html')

def dashtobsingle (request):
    return render (request,'blog-single.html')

def contact(request):
    return render (request,'contact.html')

def dashtocourse (request):
    return render (request,'course-detail.html')

def gallery(request):
    return render (request,'gallery.html')

def page404(request):
    return render (request,'404.html')

#create financial request
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_Finance_Post(request):
    data={}
    form1 = MarkForm()
    if request.method == 'POST':
        form = FinanceHelpForm(request.POST,request.FILES)
        if form.is_valid():
            addrequest = form.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
            requests = Finance_request.objects.all()
            context = {'requests':requests}
            data['html']=render_to_string('faculty/financial_request.html',{'requests':requests})
            return JsonResponse(data)
        else:
            print("not valid")
            return JsonResponse({'data':'not valid'})
    return JsonResponse({'data':'return'})

#update financial request
def update_Finance_Post(request,id):
    finance_request = Finance_request.objects.get(id=id)
    form = FinanceHelpForm(instance=finance_request)
    if request.method == 'POST':
        form = FinanceHelpForm(request.POST,request.FILES,instance=finance_request)
        if form.is_valid():
            addrequest = form.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
            return redirect('faculty-dashboard')
    context = {'form':form}
    print(finance_request)
    return render (request,'Finance/create-finance-request.html',context)

#detail descriotion of a particular financial request
def View_Detail_Of_Financia_Request(request,id):
    finance_request_detail = Finance_request.objects.get(id=id)
    context = {
        'finance_request_detail':finance_request_detail
    }
    return render(request,'faculty/financial_request_detail_page.html',context)
    



