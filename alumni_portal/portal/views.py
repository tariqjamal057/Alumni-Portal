from datetime import datetime
from email import message
from multiprocessing import context
from pipes import Template
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q

from portal.forms import FinanceHelpForm, MentorHelpForm
from portal.models import *

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
    return user.groups.filter(name='alumni').exists()

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
    if 'q' in request.GET:
        q=request.GET['q']
        requests=Finance_request.objects.filter(Q(title__icontains=q) | Q(student_name__icontains=q)).order_by('-id')
    else:
        requests = Finance_request.objects.all().order_by('-id')
    requests = Finance_request.objects.filter(posted_by = request.user).order_by('-id')
    paginator=Paginator(requests,1)
    page_num=request.GET.get('page',1)
    requests=paginator.page(page_num)
    context = {
        "requests" : requests,
    }
    return render(request,'faculty/faculty-dashboard.html',context)

@login_required()
def alumini(request):
    if 'q' in request.GET:
        q=request.GET['q']
        requests=Finance_request.objects.filter(Q(title__icontains=q) | Q(student_name__icontains=q)).order_by('-id')
    else:
        requests = Finance_request.objects.all().order_by('-id')
    context = {
        'finance_post' :  requests,
    }
    return render(request,'alumini/alumini-dashboard.html', context)

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
def create_Finance_Post(request):
    form = FinanceHelpForm()
    print("started")
    if request.method == 'POST':
        form = FinanceHelpForm(request.POST,request.FILES)
        print(form)
        print(form.is_valid())
        print("enter")
        if form.is_valid():
            addrequest = form.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
            print("work")
            return redirect('/dashboard')
    return render(request,'faculty/create_financial_request.html',{'form':form})



def update_Finance_Post(request,pk):
    req = Finance_request.objects.get(id=pk)
    updateform = FinanceHelpForm(instance=req)
    if request.method == 'POST':
        updateform = FinanceHelpForm(request.POST,request.FILES,instance=req)
        if updateform.is_valid():
            addrequest = updateform.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
            return redirect('/dashboard')
    return render(request,'faculty/update_financial_request.html',{'updateform':updateform})

def view_detail_page(request,pk):
    request_i = Finance_request.objects.get(id=pk)
    alumni_interest = Finance_request_Post_Response.objects.filter(post = request_i).order_by('-id')
    context = {
        'request_details' : request_i,
        'alumni_interest':alumni_interest
    }
    return render(request,'faculty/financial_request_detail_page.html',context)
    
    
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

# Finance Request page 
def finance_request_page(request):
    if 'q' in request.GET:
        q=request.GET['q']
        requests=Finance_request.objects.filter(Q(title__icontains=q) | Q(student_name__icontains=q) | Q(description__icontains=q)).order_by('-id')
    else:
        requests = Finance_request.objects.all().order_by('-id')
    paginator=Paginator(requests,1)
    page_num=request.GET.get('page',1)
    requests=paginator.page(page_num)
    context = {
        'finance_post' :  requests,
    }
    return render(request,'pages/alumni_as_sponser/financehelp_page.html',context)

def finance_request_detail_page(request,pk):
    request_i = Finance_request.objects.get(id=pk)
    all_requests = Finance_request.objects.all().order_by("-id")[:6]
    interest = Finance_request_Post_Response.objects.get(user_id=request.user.id,post_id=pk)
    message = Finance_request_Response_Message.objects.filter(post_response_id=interest.id).order_by('-id')[:5]
    contrib = featured_Sponser.objects.filter(user_id=request.user.id,student_name_id=interest.id)
    context = {
        'request_details' : request_i,
        'all_requests':all_requests,
        'message':message,
        'contrib':contrib,
    }
    return render(request,'pages/alumni_as_sponser/request_detail.html',context)

@csrf_exempt
def alumini_message(request):
    data = dict()
    print("working")
    id = request.POST.get('id')
    message = request.POST.get('message')
    post=Finance_request.objects.get(id=id)
    requser = request.user
    print(requser)
    interest,created = Finance_request_Post_Response.objects.get_or_create(user=request.user,post=post)
    Finance_request_Response_Message.objects.create(user_id=requser.id,post_response_id=interest.id,message=message, date=datetime.now())
    print("done")
    # return JsonResponse(data)
    print("Hello World")
    context = {
    }
    return render(request,'pages/alumni_as_sponser/alumni_chat.html',context)

@csrf_exempt
def get_alumni_message(request):
    data = dict()
    id = request.POST.get('id')
    data["id"] = id
    interest = Finance_request_Post_Response.objects.get(user_id=request.user.id,post_id=id)
    message = Finance_request_Response_Message.objects.filter(post_response_id=interest.id)
    print("hellllo")
    print(message)
    data['html'] = render_to_string('pages/alumni_as_sponser/alumni_chat.html', {'message': message,'user': request.user})
    return JsonResponse(data)



@csrf_exempt
def get_message_interest(request):
    data = dict()
    post_id = request.POST.get('post_id')
    user = request.POST.get('user')
    messages = Finance_request_Response_Message.objects.filter(post_response = post_id,user = user)
    faculty_messages = Finance_request_Response_Message.objects.filter(post_response = post_id,user = request.user.id)
    var = request.POST.get('chatfun')
    if (var):
        interestid = request.POST.get('id')
        message = request.POST.get('message')
        print(message)
        # interest = Finance_request_Post_Response.objects.get(user=user,post=post)
        Finance_request_Response_Message.objects.create(user_id=request.user.id,post_response_id=interestid,message=message, date=datetime.now())
    context = {
        'messages':messages,
        'faculty_messages':faculty_messages,
        'post_interest':post_id,
        'intest_user':user,
    }
    data['html']  = render_to_string('faculty/chat.html',context)
    return JsonResponse(data)

@csrf_exempt
def add_finance_amount(request):
    data = dict()
    print("hsajh")
    postid = request.POST.get('post_id')
    user = request.POST.get('user')
    print(postid)
    print(user)
    inst = Finance_request_Post_Response.objects.get(user_id = user,post_id = postid)
    print(inst.post_id)
    print(inst.user_id)
    print("jdkjdhkuhudfsghudf")
    context = {
        'student_name':inst.post.student_name,
        'alumni_name':inst.user.username,
        'postid':inst.post_id,
        'alumniid':inst.user_id,
    }
    data['html']  = render_to_string('faculty/add_sponser.html',context)
    return JsonResponse(data)

@csrf_exempt
def add_sponser(request):
    data = dict()
    studentname = request.POST.get('studentname')
    alumniname = request.POST.get('alumniname')
    amount = request.POST.get('amount')
    postid = request.POST.get('postid')
    alumniid = request.POST.get('alumniid')
    featured_Sponser.objects.create(student_name_id=postid,user_id=alumniid,amount=amount,date=datetime.now())
    return render(request,'faculty/add_sponser.html')


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


# Help Desk 


def help_desk(request):
    help_desk = Post.objects.all()
    context = {
        'help_desk': help_desk,
    }
    return render(request,'pages/helpdesk_page.html',context)

#create mentor help post
@csrf_exempt
def create_help_desk_post(request):
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



