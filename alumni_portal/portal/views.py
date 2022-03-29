from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from portal.forms import FinanceHelpForm, MarkForm
from portal.models import Finance_request, User

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
@csrf_exempt
def create_Finance_Post(request):
    data={}
    
    if request.method == 'POST':
        form = FinanceHelpForm(request.POST,request.FILES)
        if form.is_valid():
            addrequest = form.save(commit=False)
            addrequest.posted_by = request.user
            addrequest.save()
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

# #chat 
# @csrf_exempt
# def addChatToDatabase(request):
#     data={}
#     if request.method == 'POST':
#         chat=request.POST.get('chat')
#         id = request.POST.get('id')
#         chat_id = request.POST.get('id')
#         post = Finance_request.objects.get(id=id)
#         chat_msg = Chat_With_Staff.objects.filter(post_id = chat_id)
#         # print(chat_msg.form_user)
#         if is_alumini(request.user):
#             Chat_With_Staff.objects.create(post_id=post,form_user=request.user,to_user=post.posted_by,message=chat)
#         else:
#             Chat_With_Staff.objects.create(post_id=post,form_user=request.user,to_user=post.posted_by,message=chat)
#         print(chat_id + "  " + id)
#         msg = Chat_With_Staff.objects.filter(post_id = chat_id)
#         print(msg)
#         data["id"] = id
#         data['html']=render_to_string('faculty/chat.html',{'msg':msg})
#         data["success"] = True
#     return JsonResponse(data)

def finance_request_page(request):
    finance_requests = Finance_request.objects.all().order_by('-id')
    user = request.user
    # msg = Chat_With_Staff.objects.all()
    context = {
        'finance_requests':finance_requests,
        # 'msg':msg,
        'user':user
    }
    return render(request,'pages/financehelp_page.html',context)
