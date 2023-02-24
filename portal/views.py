from datetime import datetime
from email import message
from django.conf import settings
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
import itertools
from django.db.models import Sum

from portal.forms import FinanceHelpForm, Help_Desk_Form, MentorHelpForm
from portal.models import *

from django.contrib.auth.decorators import user_passes_test

# from portal.models import allowed_user

# Create your views here.
# def is_alumini(user):
#     return user.groups.filter(name='alumini').exists()

@login_required()
def home(request):
    user = request.user
    help_desk_post = Post.objects.all().order_by('-id')[:6]
    mentor_help_post = Tech_Help_Post.objects.all().order_by('-id')[:3]

    feautured_sponser = Featured_Sponser.objects.values('user__username').annotate(count=Sum('amount'))
    context = {
        "user":user,
        'is_alumini': is_alumini(request.user),
        'posts':help_desk_post,
        'mentor_help_post':mentor_help_post,
        'feautured_sponser':feautured_sponser,
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
    requests = Finance_request.objects.filter(posted_by = request.user).order_by('-id')
    paginator=Paginator(requests,9)
    page_num=request.GET.get('page',1)
    requests=paginator.page(page_num)
    context = {
        "requests" : requests,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'faculty/faculty-dashboard.html',context)

@login_required()
def alumini(request):
    posts = Post.objects.filter(posted_by = request.user).order_by('-id')
    paginator=Paginator(posts,9)
    page_num=request.GET.get('page',1)
    posts=paginator.page(page_num)
    context = {
        "posts" : posts,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'alumni/alumni-dashboard.html',context)

@login_required()
def student(request):
    posts = Tech_Help_Post.objects.filter(posted_by = request.user).order_by('-id')
    paginator=Paginator(posts,9)
    page_num=request.GET.get('page',1)
    posts=paginator.page(page_num)
    context = {
        "posts" : posts,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'student/student-dashboard.html',context)

def blog (request):
    return render (request,'blog-archive.html')

def blog_single (request):
    return render (request,'blog-single.html')

def contact(request):
    return render (request,'contact.html')

def course (request):
    return render (request,'course-detail.html')

def gallery(request):
    return render (request,'gallery.html')

def page404(request):
    return render (request,'404.html')

# Alumni as Sponser
# Functionality of faculty side

def faculty_post_search(request):
    data = dict()
    query = request.POST.get('query')
    requests = Finance_request.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(achievements__icontains=query) | Q(other_performance__icontains=query),posted_by = request.user)
    data['html'] = render_to_string('faculty/finance_request.html', {'requests': requests, })
    return JsonResponse(data)


def create_Finance_Post(request):
    if request.method == 'POST':
        form = FinanceHelpForm(request.POST,request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.posted_by = request.user
            form.save()
            return redirect('/dashboard')
        else:
            return render(request,'faculty/create_financial_request.html',{'form':form})
    else:
        form = FinanceHelpForm()
    return render(request,'faculty/create_financial_request.html',{'form':form})

def update_Finance_Post(request,pk):
    req = Finance_request.objects.get(id=pk)
    form = FinanceHelpForm(instance=req)
    if request.method == 'POST':
        form = FinanceHelpForm(request.POST,request.FILES,instance=req)
        if form.is_valid():
            form = form.save(commit=False)
            form.posted_by = request.user
            form.save()
            return redirect('/dashboard')
    return render(request,'faculty/update_financial_request.html',{'form':form})

def view_detail_page(request,pk):
    post = Finance_request.objects.get(id=pk)
    alumni_interest = Finance_request_Post_Response.objects.filter(post = post).order_by('-id')
    recent_intetest = Finance_request_Post_Response.objects.filter(post = post).order_by('-id')[:5]
    recent_sponsers = Featured_Sponser.objects.filter(student_name_id = post.id).order_by('-id')[:5]
    all_sponser = Featured_Sponser.objects.filter(student_name_id = post.id).order_by('-id')
    total_number_of_interest = len(alumni_interest) # Total Number of Interest Count
    number_of_sponser = len(all_sponser) # Total Number of Sponser Count
    context = {
        'request_details' : post,
        'alumni_interest':alumni_interest,
        'recent_intetest':recent_intetest,
        'recent_sponsers':recent_sponsers,
        'all_sponser':all_sponser,
        'number_of_sponser':number_of_sponser,
        'total_number_ointerest':total_number_of_interest,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'faculty/financial_request_detail_page.html',context)
    

def delete_Finance_Post(request):
    data = dict()
    id = request.POST.get('id')
    financial_request = Finance_request.objects.filter(id=id)
    financial_request.delete()
    requests = Finance_request.objects.filter(posted_by=request.user)
    data['html'] = render_to_string('faculty/finance_request.html', {'requests': requests, })
    data["success"] = True
    return JsonResponse(data)

def finance_request_chat(request,pk):
    post = Finance_request.objects.get(id=pk)
    if 'interest_search_query' in request.GET:
        interest_search_query=request.GET['interest_search_query']
        alumni_interests = Finance_request_Post_Response.objects.filter(Q(user__first_name__icontains=interest_search_query) | Q(user__last_name__icontains=interest_search_query),post = post).order_by('-id')
    else:
        alumni_interests = Finance_request_Post_Response.objects.filter(post = post).order_by('-id')
        interest_search_query = None
    users = User.objects.all()
    context = {
        'alumni_interests':alumni_interests,
        'users':users,
        'post':post,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'faculty/message.html',context)

def get_interest(request):
    data = dict()
    csrf_token = request.POST.get('csrfmiddlewaretoken')
    post_id = request.POST.get('post_id')
    user = request.POST.get('user')
    interest_user = Finance_request_Post_Response.objects.filter(post = post_id,user = user)
    context = {
        'interest_user':interest_user,
    }
    data['token'] = csrf_token
    data['html'] = render_to_string('faculty/finance_chat_header.html',context)
    return JsonResponse(data)

def get_interest_message(request):
    data = dict()
    csrf_token = request.POST.get('csrfmiddlewaretoken')
    post_id = request.POST.get('post_id')
    user = request.POST.get('user')
    interest_id = request.POST.get('interest_id')
    interest = interest_id
    messages = Finance_request_Response_Message.objects.filter(post_response__id = interest)
    faculty = request.user
    context = {
        'messages':messages,
        'post_interest':post_id,
        'intest_user':user,
        'interest':interest,
        'faculty':faculty,
    }
    data['token'] = csrf_token
    data['interest_id'] = interest_id
    data['html']  = render_to_string('faculty/user_messages.html',context,request)
    return JsonResponse(data) 

def faculty_addchat(request):
    data = dict()
    interest_id = request.POST.get('id')
    message = request.POST.get('message')
    Finance_request_Response_Message.objects.create(user_id=request.user.id,post_response_id=interest_id,message=message)
    messages = Finance_request_Response_Message.objects.filter(post_response__id = interest_id)
    context = {
        'messages':messages,
    }
    data['html']  = render_to_string('faculty/user_messages.html',context,request)
    return JsonResponse(data)

def add_finance_amount(request):
    data = dict()
    csrf_token = request.POST.get('csrfmiddlewaretoken')
    postid = request.POST.get('post_id')
    user = request.POST.get('user')
    inst = Finance_request_Post_Response.objects.get(user_id = user,post_id = postid)
    context = {
        'student_name':inst.post.name,
        'alumni_name':inst.user.username,
        'postid':inst.post_id,
        'alumniid':inst.user_id,
    }
    data['token'] = csrf_token
    data['html']  = render_to_string('faculty/add_sponser.html',context)
    return JsonResponse(data)

def add_sponser(request):
    data =dict()
    amount = request.POST.get('amount')
    post_id = request.POST.get('postid')
    alumni_id = request.POST.get('alumniid')
    Featured_Sponser.objects.create(student_name_id=post_id,user_id=alumni_id,amount=amount)
    return JsonResponse(data)


# Alumni as a sponser 
# Functionality of alumni side

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='alumni').exists())
def finance_request_page(request):
    if 'search_query' in request.GET:
        search_query=request.GET['search_query']
        requests=Finance_request.objects.filter(Q(title__icontains=search_query) | Q(name__icontains=search_query) | Q(description__icontains=search_query)).order_by('-id')
    else:
        requests = Finance_request.objects.all().order_by('-id')
        search_query = None
    paginator=Paginator(requests,9)
    page_num=request.GET.get('page',1)
    requests=paginator.page(page_num)
    context = {
        'finance_post' :  requests,
        'search_query':search_query,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/alumni_as_sponser/financehelp_page.html',context)


def finance_request_detail_page(request,pk):
    request_details = Finance_request.objects.get(id=pk)
    related_posts = Finance_request.objects.all().order_by("-id")[:6]
    if Finance_request_Post_Response.objects.filter(user_id=request.user.id,post_id=pk).exists():
        is_showed_interest = True
    else:
        is_showed_interest = False
    message = Finance_request_Response_Message.objects.filter(post_response__post=pk).order_by('-id')[:5]
    contributions = Featured_Sponser.objects.filter(user=request.user,student_name=request_details)

    context = {
        'request_details' : request_details,
        'related_posts':related_posts,
        'message':message,
        'contributions':contributions,
        'is_showed_interest':is_showed_interest,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/alumni_as_sponser/request_detail.html',context)


def alumni_as_sponser_chat(request,pk):
    post = Finance_request.objects.get(id = pk)
    messages = Finance_request_Response_Message.objects.filter(post_response__post=pk)
    contrib = Featured_Sponser.objects.filter(user_id = request.user.id , student_name_id = pk) 
    context = {
        'messages':messages,
        'contrib':contrib,
        'post':post,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/alumni_as_sponser/message.html',context)

def alumini_message(request):
    data = dict()
    post_id = request.POST.get('id')
    message = request.POST.get('message')
    post=Finance_request.objects.get(id=post_id)
    posted_by = post.posted_by.email
    requser = request.user
    interest,created = Finance_request_Post_Response.objects.get_or_create(user=request.user,post=post)
    if(created):
        from_email = settings.EMAIL_ADMIN
        to_email = [post.posted_by.email]
        subject = 'You get a new Interest from Post'
        message = 'You get a new Interest from '+ interest.user
        send_mail(
            subject,
            message,
            from_email,
            to_email,
        )
    Finance_request_Response_Message.objects.create(user=requser,post_response=interest,message=message)
    messages = Finance_request_Response_Message.objects.filter(post_response=interest)
    context = {
        'messages':messages,
    }
    data['html'] = render_to_string('pages/alumni_as_sponser/alumni_chat.html',context,request)
    return JsonResponse(data)

# Help Desk Section
#functionalty in alumni side

def alumni_post_search(request):
    data = dict()
    query = request.POST.get('query')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query),posted_by = request.user)
    data['html'] = render_to_string('alumni/help_desk_post.html', {'posts': posts, })
    return JsonResponse(data)

def create_help_desk_post(request):
    if request.method == 'POST':
        form = Help_Desk_Form(request.POST,request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.posted_by = request.user
            form.save()
            return redirect('/dashboard')
        else:
            return render(request,'alumni/create_help_desk_post.html',{'form':form})
    else:
        form = Help_Desk_Form()
    return render(request,'alumni/create_help_desk_post.html',{'form':form})

def update_help_desk_post(request,pk):
    req = Post.objects.get(id=pk)
    form = Help_Desk_Form(instance=req)
    if request.method == 'POST':
        form = Help_Desk_Form(request.POST,request.FILES,instance=req)
        if form.is_valid():
            form = form.save(commit=False)
            form.posted_by = request.user
            form.save()
            return redirect('dashboard')
    return render(request,'alumni/update_help_desk_post.html',{'form':form})

def help_desk_post_detail(request,pk):
    post = Post.objects.get(id=pk)
    interest = PostResponse.objects.filter(post = post).order_by('-id')
    recent_intetest = PostResponse.objects.filter(post = post).order_by('-id')[:5]
    context = {
        'request_details' : post,
        'alumni_interest':interest,
        'recent_intetest':recent_intetest,
        'total_number_of_interest':len(interest),
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'alumni/help_desk_post_detail_page.html',context)

def delete_help_desk_post(request):
    data = dict()
    id = request.POST.get('id')
    financial_request = Post.objects.filter(id=id)
    financial_request.delete()
    posts = Post.objects.filter(posted_by=request.user)
    data['html'] = render_to_string('alumni/help_desk_post.html', {'posts': posts, })
    data["success"] = True
    return JsonResponse(data)

def help_desk_post_chat(request,pk):
    post = Post.objects.get(id=pk)
    if 'interest_search_query' in request.GET:
        interest_search_query=request.GET['interest_search_query']
        alumni_interests = PostResponse.objects.filter(Q(user__first_name__icontains=interest_search_query) | Q(user__last_name__icontains=interest_search_query),post = post).order_by('-id')
    else:
        interests = PostResponse.objects.filter(post = post).order_by('-id')
        interest_search_query = None
    users = User.objects.all()
    context = {
        'alumni_interests': interests,
        'users':users,
        'post':post,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'alumni/message.html',context)

def get_help_desk_chat_header(request):
    data = dict()
    csrf_token = request.POST.get('csrfmiddlewaretoken')
    post_id = request.POST.get('post_id')
    user = request.POST.get('user')
    interest_user = PostResponse.objects.filter(post = post_id,user = user)
    context = {
        'interest_user':interest_user,
    }
    data['token'] = csrf_token
    data['html'] = render_to_string('alumni/help_desk_chat_header.html',context)
    return JsonResponse(data)

def help_desk_interest_message(request):
    data = dict()
    csrf_token = request.POST.get('csrfmiddlewaretoken')
    post_id = request.POST.get('post_id')
    user = request.POST.get('user')
    interest_id = request.POST.get('interest_id')
    interest = interest_id
    messages = ResponseMessage.objects.filter(post_response__id = interest)
    faculty = request.user
    context = {
        'messages':messages,
        'post_interest':post_id,
        'intest_user':user,
        'interest':interest,
        'faculty':faculty,
    }
    data['token'] = csrf_token
    data['interest_id'] = interest_id
    data['html']  = render_to_string('alumni/user_messages.html',context,request)
    return JsonResponse(data) 

def alumni_addchat(request):
    data = dict()
    interest_id = request.POST.get('id')
    message = request.POST.get('message')
    ResponseMessage.objects.create(user_id=request.user.id,post_response_id=interest_id,message=message)
    messages = ResponseMessage.objects.filter(post_response__id = interest_id)
    context = {
        'messages':messages,
    }
    data['html']  = render_to_string('alumni/user_messages.html',context,request)
    return JsonResponse(data)



# Help desk post
# functionality for for all member

@login_required()
def help_desk_page(request):
    if 'search_query' in request.GET:
        search_query=request.GET['search_query']
        posts=Post.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)).order_by('-id')
    else:
        posts = Post.objects.all().order_by('-id')
        search_query = None
    paginator=Paginator(posts,9)
    page_num=request.GET.get('page',1)
    posts=paginator.page(page_num)
    context = {
        'help_desk_post' :  posts,
        'search_query':search_query,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/help_desk_post/help_desk_page.html',context)

def help_desk_detail_page(request,pk):
    request_details = Post.objects.get(id=pk)
    related_posts = Post.objects.all().order_by("-id")[:6]
    if PostResponse.objects.filter(user_id=request.user.id,post_id=pk).exists():
        is_showed_interest = True
    else:
        is_showed_interest = False
    message = ResponseMessage.objects.filter(post_response__post=pk).order_by('-id')[:5]

    context = {
        'request_details' : request_details,
        'related_posts':related_posts,
        'message':message,
        'is_showed_interest':is_showed_interest,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/help_desk_post/request_detail.html',context)

def help_desk_chat(request,pk):
    post = Post.objects.get(id = pk)
    messages = ResponseMessage.objects.filter(post_response__post=pk)
    context = {
        'messages':messages,
        'post':post,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/help_desk_post/message.html',context)

def help_desk_users_message(request):
    data = dict()
    post_id = request.POST.get('id')
    message = request.POST.get('message')
    post=Post.objects.get(id=post_id)
    posted_by = post.posted_by.email
    requser = request.user
    interest,created = PostResponse.objects.get_or_create(user=request.user,post=post)
    if(created):
        from_email = settings.EMAIL_ADMIN
        to_email = [post.posted_by.email]
        subject = 'You get a new Interest from Post'
        message = 'You get a new Interest from '+ str(interest.user)
        send_mail(
            subject,
            message,
            from_email,
            to_email,
        )
    ResponseMessage.objects.create(user=requser,post_response=interest,message=message)
    messages = ResponseMessage.objects.filter(post_response=interest)
    context = {
        'messages':messages,
    }
    data['html'] = render_to_string('pages/help_desk_post/help_desk_chat.html',context,request)
    return JsonResponse(data)


# Mentor help Post
# functionality for the student 

def student_post_search(request):
    data = dict()
    query = request.POST.get('query')
    posts=Tech_Help_Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query),posted_by = request.user)
    data['html'] = render_to_string('student/mentor_help_post.html', {'posts': posts, })
    return JsonResponse(data)

def create_mentor_help_post(request):
    if request.method == 'POST':
        form = MentorHelpForm(request.POST,request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.posted_by = request.user
            form.save()
            return redirect('/dashboard')
        else:
            return render(request,'student/create_mentor_help_post.html',{'form':form})
    else:
        form = MentorHelpForm()
    return render(request,'student/create_mentor_help_post.html',{'form':form})

def update_mentor_help_post(request,pk):
    req = Tech_Help_Post.objects.get(id=pk)
    form = MentorHelpForm(instance=req)
    if request.method == 'POST':
        form = MentorHelpForm(request.POST,request.FILES,instance=req)
        if form.is_valid():
            form = form.save(commit=False)
            form.posted_by = request.user
            form.save()
            return redirect('dashboard')
    return render(request,'student/update_mentor_help_post.html',{'form':form})

def mentor_help_post_detail(request,pk):
    post = Tech_Help_Post.objects.get(id=pk)
    interest = Tech_Help_PostResponse.objects.filter(post = post).order_by('-id')
    recent_intetest = Tech_Help_PostResponse.objects.filter(post = post).order_by('-id')[:5]
    context = {
        'request_details' : post,
        'alumni_interest':interest,
        'recent_intetest':recent_intetest,
        'total_number_of_interest':len(interest),
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'student/mentor_help_post_detail_page.html',context)

def delete_mentor_help_post(request):
    data = dict()
    id = request.POST.get('id')
    financial_request = Tech_Help_Post.objects.filter(id=id)
    financial_request.delete()
    posts = Tech_Help_Post.objects.filter(posted_by=request.user)
    data['html'] = render_to_string('student/mentor_help_post.html', {'posts': posts, })
    data["success"] = True
    return JsonResponse(data)

def mentor_help_post_chat(request,pk):
    post = Tech_Help_Post.objects.get(id=pk)
    if 'interest_search_query' in request.GET:
        interest_search_query=request.GET['interest_search_query']
        alumni_interests = Tech_Help_PostResponse.objects.filter(Q(user__first_name__icontains=interest_search_query) | Q(user__last_name__icontains=interest_search_query),post = post).order_by('-id')
    else:
        interests = Tech_Help_PostResponse.objects.filter(post = post).order_by('-id')
        interest_search_query = None
    users = User.objects.all()
    context = {
        'alumni_interests': interests,
        'users':users,
        'post':post,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'student/message.html',context)

def get_mentor_help_chat_header(request):
    data = dict()
    csrf_token = request.POST.get('csrfmiddlewaretoken')
    post_id = request.POST.get('post_id')
    user = request.POST.get('user')
    interest_user = Tech_Help_PostResponse.objects.filter(post = post_id,user = user)
    context = {
        'interest_user':interest_user,
    }
    data['token'] = csrf_token
    data['html'] = render_to_string('student/mentor_help_chat_header.html',context)
    return JsonResponse(data)

def mentor_help_interest_message(request):
    data = dict()
    csrf_token = request.POST.get('csrfmiddlewaretoken')
    post_id = request.POST.get('post_id')
    user = request.POST.get('user')
    interest_id = request.POST.get('interest_id')
    interest = interest_id
    messages = Tech_Help_ResponseMessage.objects.filter(post_response__id = interest)
    faculty = request.user
    context = {
        'messages':messages,
        'post_interest':post_id,
        'intest_user':user,
        'interest':interest,
        'faculty':faculty,
    }
    data['token'] = csrf_token
    data['interest_id'] = interest_id
    data['html']  = render_to_string('student/user_messages.html',context,request)
    return JsonResponse(data) 

def mentor_addchat(request):
    data = dict()
    interest_id = request.POST.get('id')
    message = request.POST.get('message')
    Tech_Help_ResponseMessage.objects.create(user_id=request.user.id,post_response_id=interest_id,message=message)
    messages = Tech_Help_ResponseMessage.objects.filter(post_response__id = interest_id)
    context = {
        'messages':messages,
    }
    data['html']  = render_to_string('student/user_messages.html',context,request)
    return JsonResponse(data)




# Help desk post
# functionality for the alumni
@login_required()
def mentor_help_page(request):
    if 'search_query' in request.GET:
        search_query=request.GET['search_query']
        posts=Tech_Help_Post.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)).order_by('-id')
    else:
        posts = Tech_Help_Post.objects.all().order_by('-id')
        search_query = None
    paginator=Paginator(posts,9)
    page_num=request.GET.get('page',1)
    posts=paginator.page(page_num)
    context = {
        'help_desk_post' :  posts,
        'search_query':search_query,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/alumni_as_mentor/mentor_help_page.html',context)

def mentor_help_detail_page(request,pk):
    request_details = Tech_Help_Post.objects.get(id=pk)
    related_posts = Tech_Help_Post.objects.all().order_by("-id")[:6]
    if Tech_Help_PostResponse.objects.filter(user_id=request.user.id,post_id=pk).exists():
        is_showed_interest = True
    else:
        is_showed_interest = False
    message = Tech_Help_ResponseMessage.objects.filter(post_response__post=pk).order_by('-id')[:5]

    context = {
        'request_details' : request_details,
        'related_posts':related_posts,
        'message':message,
        'is_showed_interest':is_showed_interest,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/alumni_as_mentor/request_detail.html',context)

def mentor_help_chat(request,pk):
    post = Tech_Help_Post.objects.get(id = pk)
    messages = Tech_Help_ResponseMessage.objects.filter(post_response__post=pk)
    context = {
        'messages':messages,
        'post':post,
        'is_alumini': is_alumini(request.user),
    }
    return render(request,'pages/alumni_as_mentor/message.html',context)

def mentor_help_users_message(request):
    data = dict()
    post_id = request.POST.get('id')
    message = request.POST.get('message')
    post=Tech_Help_Post.objects.get(id=post_id)
    posted_by = post.posted_by.email
    requser = request.user
    interest,created = Tech_Help_PostResponse.objects.get_or_create(user=request.user,post=post)
    if(created):
        from_email = settings.EMAIL_ADMIN
        to_email = [post.posted_by.email]
        subject = 'You get a new Interest from Post'
        message = 'You get a new Interest from '+ str(interest.user)
        send_mail(
            subject,
            message,
            from_email,
            to_email,
        )
    Tech_Help_ResponseMessage.objects.create(user=requser,post_response=interest,message=message)
    messages = Tech_Help_ResponseMessage.objects.filter(post_response=interest)
    context = {
        'messages':messages,
    }
    data['html'] = render_to_string('pages/alumni_as_mentor/mentor_help_chat.html',context,request)
    return JsonResponse(data)