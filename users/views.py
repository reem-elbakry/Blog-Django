from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, ProfileForm, LoginForm, EditProfileForm, ChangePasswordForm
from .util_funcs import isLocked
from posts import views as post_views
from .models import Profile
from django.contrib.auth import login, authenticate,  update_session_auth_hash
from django.contrib.auth.models import User
from .logger import log
from django.core.mail import send_mail
from .util_funcs import delete_profile_pic
import os


def register(request):
    if(not request.user.is_authenticated):
        if request.method == "POST":
            user_form = RegistrationForm(request.POST)
            # get the form and the upladed files
            profile_form = ProfileForm(request.POST, request.FILES)
            if user_form.is_valid():
                user = user_form.save()  # save the user into database and return it
                # get the profile of the created user
                profile = Profile.objects.get(user=user)
                # get the uploaded picture if any
                file = request.FILES.get("profile_pic")
                if(file != None):
                    profile.profile_pic = file  # add the provided pic to that user profile
                profile.bio = request.POST["bio"]
                profile.save()  # save the updates to user profile
                log(profile.profile_pic.url)
                log("created a new user successfully with username: " +
                    user.username)  # for debugging purposes
                user = authenticate(
                    username=request.POST["username"], password=request.POST["password1"])
                if user is not None:
                    login(request, user)
                    try:
                        send_mail('Welcome to our blog', 'Django Blog team welcomes you to our blog .',
                                  'dproject.os40@gmail.com', [user.email], fail_silently=False,)
                    except Exception as ex:
                        log("couldn't send email message"+str(ex))

                    # redirect to user profile page
                    return HttpResponseRedirect("/users/profile")
                else:
                    log("cannot login from refistration form")
            else:
                log("invalid registration form")  # for debugging purposes
        else:
            user_form = RegistrationForm()
            profile_form = ProfileForm()
        context = {"user_form": user_form, "profile_form": profile_form}
        return render(request, 'users/register.html', context)
    else:
        return HttpResponseRedirect("/")



def login_view(request):
   
    if(not request.user.is_authenticated):  # check if user is already logged in
        if request.method == "POST":
            # using named parameter as request.Post isn't the first parameter by default
            login_form = LoginForm(data=request.POST)
            if(login_form.is_valid()):
                username = request.POST['username']
                password = request.POST["password"]
                # authenticate the user with provided data
                user = authenticate(username=username, password=password)
                if user is not None:  # user authenticated
                    if(isLocked(user)):
                        log(user.username + " blocked user")
                        # redirect the user to a custom page for blocked users
                        return HttpResponseRedirect("/users/blocked")
                    else:
                        login(request, user)
                        log(user.username + " logged in successfully")
                        # redirect to user homepage
                        return HttpResponseRedirect("/")
                else:
                    log("cannot login from login page")

            else:
                log("invalid login form")
        else:
            login_form = LoginForm()
        context = {"login_form": login_form}
        return render(request, 'users/login.html', context)
    else:
        return HttpResponseRedirect("/")

def profile(request):
    if(request.user.is_authenticated):
        user = request.user  # get the current user
        # get the profile related to that user
        userprofile = Profile.objects.get(user=user)
        context = {"user": user, "userprofile": userprofile}
        return render(request, "users/profile.html", context)
    else:
        return HttpResponseRedirect("/")   


def edit_profile(request):
    if(request.user.is_authenticated):
        if request.method == "POST":
            edit_form = EditProfileForm(data=request.POST)
            profile_form = ProfileForm(request.POST, request.FILES)
            user = request.user
            if(edit_form.is_valid()):
                log("valid edit form")
                file = request.FILES.get("profile_pic")
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.profile.bio = request.POST["bio"]
                if(file != None):
                    if(user.profile.profile_pic != None):
                        delete_profile_pic(user.profile.profile_pic)
                    user.profile.profile_pic = file
                user.save()
                user.profile.save()
                log(user.username + "  updated his profile")
                return HttpResponseRedirect("/users/profile")
            else:
                log("invalid change form")
                return HttpResponseRedirect("/")
        else:
            user = request.user
            user_data = {"first_name": user.first_name,
                         "last_name": user.last_name}
            bio_data = {"bio": user.profile.bio}
            edit_form = EditProfileForm(data=user_data)
            profile_form = ProfileForm(data=bio_data)
            context = {"edit_form": edit_form, "profile_form": profile_form}
            return render(request, "users/edit.html", context)
    else:
        return HttpResponseRedirect("/")





