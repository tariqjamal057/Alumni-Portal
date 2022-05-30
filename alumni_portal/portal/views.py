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

from portal.forms import FinanceHelpForm, Help_Desk_Form, MentorHelpForm
from portal.models import *

# from portal.models import allowed_user

# Create your views here.
def is_alumini(user):
    return user.groups.filter(name='alumini').exists()


def home(request):
    user = request.user
    help_desk_post = Post.objects.all().order_by('-id')[:6]
    mentor_help_post = Tech_Help_Post.objects.all().order_by('-id')[:3]
    context = {
        "user":user,
        'is_alumini': is_alumini(request.user),
        'posts':help_desk_post,
        'mentor_help_post':mentor_help_post,
    }
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
        requests = Finance_request.objects.filter(posted_by = request.user).order_by('-id')
    for req in requests:
        if req.posted_by != request.user:
            requests = Finance_request.objects.filter(posted_by = request.user).order_by('-id')
    paginator=Paginator(requests,9)
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
        posts=Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by('-id')
    else:
        posts = Post.objects.filter(posted_by = request.user).order_by('-id')
    for post in posts:
        if post.posted_by != request.user:
            posts = Post.objects.filter(posted_by = request.user).order_by('-id')
    paginator=Paginator(posts,9)
    page_num=request.GET.get('page',1)
    posts=paginator.page(page_num)
    context = {
        'posts' :  posts,
    }
    return render(request,'alumini/alumini-dashboard.html', context)

@login_required()
def student(request):
    if 'q' in request.GET:
        q=request.GET['q']
        posts=Tech_Help_Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by('-id')
    else:
        posts = Tech_Help_Post.objects.filter(posted_by = request.user).order_by('-id')
    for post in posts:
        if post.posted_by != request.user:
            posts = Tech_Help_Post.objects.filter(posted_by = request.user).order_by('-id')
    paginator=Paginator(posts,9)
    page_num=request.GET.get('page',1)
    posts=paginator.page(page_num)
    context = {
        'posts' :  posts,
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

# Alumni as Sponser

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
    recent_intetest = Finance_request_Post_Response.objects.filter(post = request_i).order_by('-id')[:5]  
    amount = featured_Sponser.objects.filter(student_name_id = request_i.id).order_by('-id')[:5]
    all_sponser = featured_Sponser.objects.filter(student_name_id = request_i.id).order_by('-id')
    context = {
        'request_details' : request_i,
        'alumni_interest':alumni_interest,
        'recent_intetest':recent_intetest,
        'amounts':amount,
        'all_sponser':all_sponser,
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
    data['html'] = render_to_string('faculty/faculty-dashboard.html', {'requests': requests, })
    data["success"] = True
    return JsonResponse(data)

# Finance Request page 
def finance_request_page(request):
    if 'q' in request.GET:
        q=request.GET['q']
        requests=Finance_request.objects.filter(Q(title__icontains=q) | Q(student_name__icontains=q) | Q(description__icontains=q)).order_by('-id')
    else:
        requests = Finance_request.objects.all().order_by('-id')
    paginator=Paginator(requests,9)
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
    # data = dict()
    # studentname = request.POST.get('studentname')
    # alumniname = request.POST.get('alumniname')
    amount = request.POST.get('amount')
    postid = request.POST.get('postid')
    alumniid = request.POST.get('alumniid')
    featured_Sponser.objects.create(student_name_id=postid,user_id=alumniid,amount=amount,date=datetime.now())
    return render(request,'faculty/add_sponser.html')


# Help Desk Section

#create help desk post
def create_help_desk_post(request):
    form = Help_Desk_Form()
    print("Help desk create post working")
    if request.method == 'POST':
        form = Help_Desk_Form(request.POST,request.FILES)
        if form.is_valid():
            addpost = form.save(commit=False)
            addpost.posted_by = request.user
            addpost.save()
            print("work")
            return redirect('/dashboard')
    return render(request,'alumini/create_post.html',{'form':form})

def update_help_desk_post(request,pk):
    req = Post.objects.get(id=pk)
    updateform = Help_Desk_Form(instance=req)
    if request.method == 'POST':
        updateform = Help_Desk_Form(request.POST,request.FILES,instance=req)
        if updateform.is_valid():
            addpost = updateform.save(commit=False)
            addpost.posted_by = request.user
            addpost.save()
            return redirect('/dashboard')
    return render(request,'alumini/update_post.html',{'updateform':updateform})

# delete help desk post
def delete_post(request):
    data = dict()
    id = request.POST.get('id')
    post = Post.objects.filter(id=id)
    post.delete()
    data["id"] = id
    post = Post.objects.filter(posted_by=request.user)
    data['html'] = render_to_string('alumini/alumini-dashboard.html', {'post': post, })
    data["success"] = True
    return JsonResponse(data)

def post_detail_page(request,pk):
    post = Post.objects.get(id=pk)
    user_interest = PostResponse.objects.filter(post = post).order_by('-id')  
    recent_intetest = PostResponse.objects.filter(post = post).order_by('-id')[:5]
    context = {
        'post':post,
        'user_interest':user_interest,
        'recent_intetest':recent_intetest,
    }
    return render(request,'alumini/detail_page.html',context)


def help_desk_page(request):
    if 'q' in request.GET:
        q=request.GET['q']
        posts=Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by('-id')
    else:
        posts = Post.objects.all().order_by('-id')
    paginator=Paginator(posts,9)
    page_num=request.GET.get('page',1)
    posts=paginator.page(page_num)
    context = {
        'posts' :  posts,
    }
    return render(request,'pages/help_desk_post/post.html',context)

def post_detail(request,pk):
    post = Post.objects.get(id=pk)
    all_post = Post.objects.all().order_by("-id")[:6]
    context = {
        'post' : post,
        'all_post':all_post,
        'is_alumni': is_alumini(request.user),
        'is_faculty': is_faculty(request.user),
        'is_student':is_student(request.user),
    }
    return render(request,'pages/help_desk_post/post_detail.html',context)

@csrf_exempt
def user_message(request):
    data = dict()
    id = request.POST.get('id')
    message = request.POST.get('message')
    post=Post.objects.get(id=id)
    requser = request.user
    interest,created = PostResponse.objects.get_or_create(user=request.user,post=post)
    ResponseMessage.objects.create(user_id=requser.id,post_response_id=interest.id,message=message, date=datetime.now())
    print("done")
    print("Hello World")
    context = {
    }
    data['html'] =  render_to_string('pages/help_desk_post/chat.html',context)
    return JsonResponse(data)

@csrf_exempt
def get_user_message(request):
    data = dict()
    id = request.POST.get('id')
    data["id"] = id
    interest = PostResponse.objects.get(user_id=request.user.id,post_id=id)
    message = ResponseMessage.objects.filter(post_response_id=interest.id)
    print("hellllo")
    print(message)
    data['html'] = render_to_string('pages/help_desk_post/chat.html', {'message': message,'user': request.user})
    return JsonResponse(data)

@csrf_exempt
def get_user_interest(request):
    data = dict()
    post_id = request.POST.get('post_id')
    user = request.POST.get('user')
    print("view working")
    print(post_id)
    print(user)
    messages = ResponseMessage.objects.filter(post_response = post_id,user = user)
    user_messages = ResponseMessage.objects.filter(post_response = post_id,user = request.user.id)
    print("printing")
    print(messages)
    print(user_messages)
    var = request.POST.get('chat')
    if (var):
        interestid = request.POST.get('id')
        message = request.POST.get('message')
        print(message)
        ResponseMessage.objects.create(user_id=request.user.id,post_response_id=interestid,message=message, date=datetime.now())
    context = {
        'messages':messages,
        'user_messages':user_messages,
        'post_interest':post_id,
        'intest_user':user,
    }
    data['html']  = render_to_string('alumini/user_chat.html',context)
    return JsonResponse(data)



# Alumni as mentor 

#create mentor help post
def create_mentor_help_post(request):
    form = MentorHelpForm()
    print("started")
    if request.method == 'POST':
        form = MentorHelpForm(request.POST,request.FILES)
        print(form)
        print(form.is_valid())
        print("enter")
        if form.is_valid():
            addrequest = form.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
            print("work")
            return redirect('/dashboard')
    return render(request,'student/create_post.html',{'form':form})

# update mentor help post
def update_mentor_help_post(request,pk):
    req = Tech_Help_Post.objects.get(id=pk)
    updateform = MentorHelpForm(instance=req)
    if request.method == 'POST':
        updateform = MentorHelpForm(request.POST,request.FILES,instance=req)
        if updateform.is_valid():
            addpost = updateform.save(commit=False)
            addpost.posted_by = request.user
            addpost.save()
            return redirect('/dashboard')
    return render(request,'student/update_post.html',{'updateform':updateform})

# delete mentor help post
@csrf_exempt
def delete_mentor_help_post(request):
    data = dict()
    id = request.POST.get('id')
    post = Tech_Help_Post.objects.filter(id=id)
    post.delete()
    data["id"] = id
    post = Tech_Help_Post.objects.filter(posted_by=request.user)
    data['html'] = render_to_string('student/student-dashboard.html', {'post': post, })
    data["success"] = True
    return JsonResponse(data)

def mentorhelp_post_detailpage(request,pk):
    post = Tech_Help_Post.objects.get(id=pk)
    # user_interest = PostResponse.objects.filter(post = post).order_by('-id')  
    # recent_intetest = PostResponse.objects.filter(post = post).order_by('-id')[:5]
    context = {
        'post':post,
        # 'user_interest':user_interest,
        # 'recent_intetest':recent_intetest,
    }
    return render(request,'student/detail_post.html',context)

def mentor_help_page(request):
    if 'q' in request.GET:
        q=request.GET['q']
        posts=Tech_Help_Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by('-id')
    else:
        posts = Tech_Help_Post.objects.all().order_by('-id')
    paginator=Paginator(posts,9)
    page_num=request.GET.get('page',1)
    posts=paginator.page(page_num)
    context = {
        'posts' :  posts,
    }
    return render(request,'pages/alumni_as_mentor/mentorhelp_page.html',context)

def mentorhelp_post_details(request,pk):
    post = Tech_Help_Post.objects.get(id=pk)
    all_post = Tech_Help_Post.objects.all().order_by("-id")[:6]
    context = {
        'post' : post,
        'all_post':all_post,
    }
    return render(request,'pages/alumni_as_mentor/post_detail.html',context)

@csrf_exempt
def mentor_message(request):
    data = dict()
    id = request.POST.get('id')
    message = request.POST.get('message')
    post=Tech_Help_Post.objects.get(id=id)
    requser = request.user
    interest,created = Tech_Help_PostResponse.objects.get_or_create(user=request.user,post=post)
    Tech_Help_ResponseMessage.objects.create(user_id=requser.id,post_response_id=interest.id,message=message, date=datetime.now())
    print("done")
    print("Hello World")
    context = {
    }
    data['html'] =  render_to_string('pages/help_desk_post/chat.html',context)
    return JsonResponse(data)

@csrf_exempt
def get_mentor_message(request):
    data = dict()
    id = request.POST.get('id')
    data["id"] = id
    interest = Tech_Help_PostResponse.objects.get(user_id=request.user.id,post_id=id)
    message = Tech_Help_ResponseMessage.objects.filter(post_response_id=interest.id)
    print("hellllo")
    print(message)
    data['html'] = render_to_string('pages/help_desk_post/chat.html', {'message': message,'user': request.user})
    return JsonResponse(data)