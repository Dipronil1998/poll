from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .forms import UserRegistrationForm,EditProfileForm,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash


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
                    user = User.objects.create_user(
                        username=username, password=password1, email=email)
                    messages.success(
                        request, f'Thanks for registering {user.username}!', extra_tags='alert alert-success alert-dismissible fade show')
                    return redirect('accounts:login')
                
        else:
            form = UserRegistrationForm()
        context={'form':form}
        return render(request,'accounts/register.html',context)



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


#EditAdminProfileForm
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


def user(request):
    users= User.objects.all()
    context={'users':users}
    return render(request,'accounts/user.html',context)


def userdetails(request, id):
    p=User.objects.get(pk=id)
    form=EditAdminProfileForm(instance=p) 
    context={'form':form}
    return render(request,'accounts/userdetails.html',context)


