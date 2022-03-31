from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from portal.forms import FinanceHelpForm, MarkForm, MentorHelpForm
from portal.models import Finance_request, Finance_request_Post_Response, Tech_Help_Post, User

# from portal.models import allowed_user

# Create your views here.
def is_alumini(user):
    return user.groups.filter(name='alumini').exists()


def home(request):
    user = request.user
    context = {"user":user,'is_alumini': is_alumini(request.user)}
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
    requests = Finance_request.objects.filter(posted_by = request.user)
    # finance_request = Finance_request.objects.get(id=id)
    # updateform = FinanceHelpForm(instance=finance_request)
    context = {
        "requests" : requests,
        "form":form,
        # "updateform":updateform,
    }
    return render(request,'faculty/faculty-dashboard.html',context)

@login_required()
def alumini(request):
    return render(request,'alumini/alumini-dashboard.html')

@login_required()
def student(request):
    mentor_help_post_form = MentorHelpForm()
    mentor_help_posts = Tech_Help_Post.objects.filter(posted_by = request.user)
    context = {
        'mentor_help_post_form':mentor_help_post_form,
        'mentor_help_posts':mentor_help_posts,
    }
    return render(request,'student/student-dashboard.html',context)

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
@csrf_exempt
def create_Finance_Post(request):
    data={}
    
    if request.method == 'POST':
        form = FinanceHelpForm(request.POST,request.FILES)
        if form.is_valid():
            addrequest = form.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
            print("saved")
            requests = Finance_request.objects.filter(posted_by=request.user)
            data['html']=render_to_string('faculty/financial_request.html',{'requests':requests})
            return JsonResponse(data)
        else:
            print("not valid")
            return JsonResponse({'data':'not valid'})
    return JsonResponse({'data':'return'})

#update financial request
@csrf_exempt
def update_Finance_Post(request):
    data={}
    try:
        if request.POST.get('type')=='get':
            id = request.POST.get('id')
            print("Id in update = "+id)
            finance_request = Finance_request.objects.get(id=id)
            updateform = FinanceHelpForm(instance=finance_request)
            data['id'] = id
            data['html']=render_to_string('faculty/update_financial_request.html',{'updateform':updateform})
            return JsonResponse(data)
        else:
            print("Updated")
            form=request.POST.get('form')
            id=request.POST.get('id')
            print(" id "+id)
            finance_request = Finance_request.objects.get(id=id)
            updateform = FinanceHelpForm(form,instance=finance_request)
            print(updateform)
            if updateform.is_valid():
                addrequest = updateform.save(commit=False)
                addrequest.posted_by = request.user
                addrequest.save()
                requests = Finance_request.objects.filter(posted_by = request.user)
                data['id'] = id
                data['html']=render_to_string('faculty/financial_request.html',{'requests':requests})
                return JsonResponse(data)
            else:
                # data['form'] = ren 
                return JsonResponse({'data':'not valid'})
        return JsonResponse(data)

    except:
        print('working')
        id = request.POST.get('id')
        print("id in except = ")
        print(id)
        finance_request = Finance_request.objects.get(id=id)
        updateform = FinanceHelpForm(request.POST,request.FILES,instance=finance_request)
        if updateform.is_valid():
            addrequest = updateform.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
            requests = Finance_request.objects.filter(posted_by = request.user)
            
            return JsonResponse(data)
        else:
            # data['form'] = ren 
            return JsonResponse({'data':'not valid'})

    
    
# delete financial Request 
def delete_Finance_Post(request):
    data = dict()
    id = request.POST.get('id')
    financial_request = Finance_request.objects.filter(id=id)
    financial_request.delete()
    data["id"] = id
    requests = Finance_request.objects.filter(posted_by=request.user)
    data['html'] = render_to_string('faculty/financial_request.html', {'requests': requests, })
    data["success"] = True
    return JsonResponse(data)

#Message 
@csrf_exempt
def addResponse_Message(request):
    data = dict()
    id = request.POST.get('id')
    message = request.POST.get('message')
    if is_alumini(request.user):
        interest = Finance_request_Post_Response.objects.get_or_create(user)
    print(message)
    print(id)
    return render(request,'pages/financehelp_page.html')

def finance_request_page(request):
    finance_requests = Finance_request.objects.all().order_by('-id')
    user = request.user
    context = {
        'finance_requests':finance_requests,
        'user':user
    }
    return render(request,'pages/financehelp_page.html',context)



# student section 

#create mentor help post
@csrf_exempt
def create_mentor_post(request):
    data={}
    
    if request.method == 'POST':
        form = MentorHelpForm(request.POST,request.FILES)
        if form.is_valid():
            addpost = form.save(commit=False)
            addpost.user = request.user
            addpost.posted_by = request.user
            addpost.save()
            mentor_help_posts = Tech_Help_Post.objects.filter(posted_by=request.user)
            data['html']=render_to_string('student/mentor_help.html',{'mentor_help_posts':mentor_help_posts})
            return JsonResponse(data)
        else:
            print("not valid")
            return JsonResponse({'data':'not valid'})
    return JsonResponse({'data':'return'})

#update mentor help post
@csrf_exempt
def update_mentor_post(request):
    data={}
    try:
        if request.POST.get('type')=='get':
            id = request.POST.get('id')
            finance_request = Finance_request.objects.get(id=id)
            updateform = FinanceHelpForm(instance=finance_request)
            data['id'] = id
            data['html']=render_to_string('faculty/update_financial_request.html',{'updateform':updateform})
            return JsonResponse(data)
        else:
            print("Updated")
            form=request.POST.get('form')
            print(form)
            id=request.POST.get('id')
            print(id)
            finance_request = Finance_request.objects.get(id=id)
            updateform = FinanceHelpForm(form,instance=finance_request)
            print(updateform)
            if updateform.is_valid():
                addrequest = updateform.save(commit=False)
                addrequest.posted_by = request.user
                addrequest.save()
                requests = Finance_request.objects.filter(posted_by = request.user)
            else:
                # data['form'] = ren 
                return JsonResponse({'data':'not valid'})
        return JsonResponse(data)

    except:
        print('working')
        id = request.POST.get('id')
        print("id in except = ")
        print(id)
        finance_request = Finance_request.objects.get(id=id)
        updateform = FinanceHelpForm(request.POST,request.FILES,instance=finance_request)
        if updateform.is_valid():
            addrequest = updateform.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
            requests = Finance_request.objects.filter(posted_by = request.user)
            
            return JsonResponse(data)
        else:
            # data['form'] = ren 
            return JsonResponse({'data':'not valid'})

    
    
# delete mentor help post 
def delete_mentor_post(request):
    data = dict()
    id = request.POST.get('id')
    student_post = Tech_Help_Post.objects.filter(id=id)
    student_post.delete()
    data["id"] = id
    mentor_help_posts = Tech_Help_Post.objects.filter(posted_by=request.user)
    data['html'] = render_to_string('student/mentor_help.html', {'mentor_help_posts': mentor_help_posts, })
    data["success"] = True
    return JsonResponse(data)

# All Mentor help posts 
def alumini_as_mentor_page(request):
    mentor_help_posts = Tech_Help_Post.objects.all().order_by('-id')
    user = request.user
    context = {
        'mentor_help_posts':mentor_help_posts,
        'user':user
    }
    return render(request,'pages/mentorhelp_page.html',context)




# Load more 
def load_more(request):
    offset=int(request.POST['offset'])
    limit=5
    posts=Finance_request.objects.all()[offset:limit+offset]
    totalData=Finance_request.objects.count()
    data={}
    posts_json=serializers.serialize('json',posts)
    return JsonResponse(data={
        'requests':posts_json,
        'totalResult':totalData
    })