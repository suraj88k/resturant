from django.db import models
from .models import *
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
import re

# Create your views here.
def index(request):
  
    category= Category.objects.all() # type: ignore
    # momo= Momo.objects.all() # type: ignore

    cateid=request.GET.get("category") 

    if cateid:
        momo=Momo.objects.filter(category=cateid)

    else:
        momo=Momo.objects.all()

    context={
        'category':category,
        'momo':momo
}
    return render(request, 'core/index.html',context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save to DB
        Contact.objects.create(name=name, email=email, phone=phone, message=message)

        # Send email to user
        send_mail(
            subject='Thank you for contacting us!',
            message=f'Dear {name},\n\nThank you for reaching out. We will get back to you shortly.\n\nYour Message:\n{message}',
            from_email='youremail@example.com',  # Replace with your email
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('contact')  # redirect after successful submission

    return render(request, 'core/contact.html')

@login_required(login_url='log_in')


def about(request):
    return render(request, 'core/about.html')

@login_required(login_url='log_in')
def menu(request):
    return render(request, 'core/menu.html')

def services(request):
    return render(request, 'core/services.html')

'''
===================

Authentication part: Start
===================
'''

def register(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password1 == password:

            error=[]

            if User.objects.filter(username=username).exists():
                error.append('username is already exists!!!')
               
            if User.objects.filter(email=email).exists():
                error.append('email is already exists!!!')

            if not re.search(r"[A-Z]",password):
                error.append('password must contain at least one upper case')

            if not re.search(r"\d",password):
                error.append('password must contain at least one digit case')
            
            
            if not re.search(r"[!@#$%^&*(),.?:{}|<>]", password):
                error.append('password must contain at least one special character')
            
            try:
                validate_password(password)

                if not error:

                    User.objects.create_user(first_name = fname, last_name = lname, username = username, email = email, password = password)
                    messages.success(request, 'Your account is succesfully registered!!!')
                    return redirect('log_in')
                
                else:
                    for i in error:
                        messages.error(request,i)
                    return redirect('register')
            
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request,i)
                    return redirect('register')
                    
        else:
            messages.error(request, 'password and confirm password does not match')
            return redirect('register')

    return render(request, 'accounts/register.html')


def log_in(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        remember_me=request.POST.get('remember_me')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'username is not registered')
            return redirect(log_in)

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            if remember_me: 
                request.session.set_expiry(1200000000)
            
            else:
                request.session.set_expiry(0)

            next=request.POST.get('next','')
            return redirect(next if next else'index')
        else:
            messages.error(request,"password invalid")
            return redirect(log_in)
        
    
    next=request.GET.get('next','')

        
    return render(request, 'accounts/login.html',{'next':next})


def log_out(request):
    logout(request)
    return redirect('log_in')



def privacy(request):
    return render(request, 'footer/privacy.html')


def terms_condition(request):
    return render(request, 'footer/terms_condition.html')

@login_required(login_url="log_in")
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
        
    return render(request,'accounts/password_change.html',{'form':form})


'''
===================

Authentication part: End
===================
'''
# pip freeze > requiremnets.text
# pip install -r  requirements.txt

print("this is for testing git hub")