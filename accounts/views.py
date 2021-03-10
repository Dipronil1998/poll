from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .forms import UserRegistrationForm,EditProfileForm,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
import random
from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Username Or Password is incorrect!!",
                    extra_tags='alert alert-warning alert-dismissible fade show')

        return render(request,'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')



def create_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            check1 = False
            check2 = False
            check3 = False
            get_otp=request.POST.get('otp')
            if get_otp:
                get_usr=request.POST.get('usr')
                usr=User.objects.get(username=get_usr)
                if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                    usr.is_active=True
                    usr.save()
                    messages.success(
                        request, f'Thanks for registering {usr.username}!', extra_tags='alert alert-success alert-dismissible fade show')
                    return redirect('accounts:login')
                else:
                    messages.error(request, 'OTP doesn\'t matched',
                            extra_tags='alert alert-warning alert-dismissible fade show')
                    return render(request,'accounts/register.html',{'otp':True, 'usr':usr})   

            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']

                if password1 != password2:
                    check1 = True
                    messages.error(request, 'Password doesn\'t matched',
                                extra_tags='alert alert-warning alert-dismissible fade show')

                if User.objects.filter(username=username).exists():
                    check2 = True
                    messages.error(request, 'Username already exists',
                                extra_tags='alert alert-warning alert-dismissible fade show')

                if User.objects.filter(email=email).exists():
                    check3 = True
                    messages.error(request, 'Email already registered',
                                extra_tags='alert alert-warning alert-dismissible fade show')
                                
                if check1 or check2 or check3:
                    messages.error(
                        request, "Registration Failed", extra_tags='alert alert-warning alert-dismissible fade show')
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.is_active=False
                    user.save()
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=user, otp=user_otp)
                    mess= f'Hello {user.username},\nYour OTP is: {user_otp}'
                    send_mail(
                        "Verify Your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    return render(request,'accounts/register.html',{'otp':True, 'usr':user})
                    #messages.success(
                    #    request, f'Thanks for registering {user.username}!', extra_tags='alert alert-success alert-dismissible fade show')
                    #return redirect('accounts:login')
                
        else:
            form = UserRegistrationForm()
        context={'form':form}
        return render(request,'accounts/register.html',context)


@login_required()
def changepassword(request):
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(
                    request, "Password changed successfully", extra_tags='alert alert-success alert-dismissible fade show')
            logout(request)
            return redirect('accounts:login')
        else:
            messages.error(
                        request, "Password is not change", extra_tags='alert alert-warning alert-dismissible fade show')
            return redirect('accounts:changepassword')
    else:
         form=PasswordChangeForm(user=request.user)
    context={'form':form}
    return render(request,'accounts/changepassword.html',context)


def contact(request):
    context={}
    return render(request,'accounts/contactus.html',context)


@login_required()
def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser == True:
                form=EditAdminProfileForm(request.POST,instance=request.user)
                users= User.objects.all()
            else:
                form=EditProfileForm(request.POST,instance=request.user) 
                users= None
            if form.is_valid():
                messages.success(
                    request, "Profile saved successfully", extra_tags='alert alert-success alert-dismissible fade show')
                form.save()
        else:
            if request.user.is_superuser == True:
                form=EditAdminProfileForm(instance=request.user) 
                users= User.objects.all()
            else:
                form=EditProfileForm(instance=request.user)
                users= None
        context={'form':form, 'users':users}
        return render(request,'accounts/profile.html',context)

@login_required()
def user(request):
    users= User.objects.all()
    context={'users':users}
    return render(request,'accounts/user.html',context)


@login_required()
def userdetails(request, id):
    p=User.objects.get(pk=id)
    form=EditAdminProfileForm(instance=p)
    if request.method == 'POST':
        form=EditAdminProfileForm(request.POST,instance=p)
        if form.is_valid():
            messages.success(
                request, "Profile saved successfully", extra_tags='alert alert-success alert-dismissible fade show')
            form.save()
    context={'form':form}
    return render(request,'accounts/userdetails.html',context)


@login_required()
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    messages.success(request, "User Deleted successfully",
                     extra_tags='alert alert-success alert-dismissible fade show')
    users= User.objects.all()
    context={'users':users}
    return render(request,'accounts/user.html',context)