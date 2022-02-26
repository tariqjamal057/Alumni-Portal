from django.shortcuts import render, redirect
#from django.contrib import login,authenticate
from .models import Authentication

# Create your views here.
def Home(request):
    return render(request,'index.html')
    
def login(request):
    context = {}
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = Authentication.empAuth_objects.get(username="User1",password="KarpagamTech")
                if user is not None:               
                    return render(request, 'Dashboard.html')
                else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username,password))
     
                    return redirect('/')
            except Exception as identifier:
                
                return redirect('/')
     
    else:
            return render(request, 'accounts/login.html')