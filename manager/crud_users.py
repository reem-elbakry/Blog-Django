from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.models import Profile
from django.contrib.auth.models import User
from users.util_funcs import *
from django.core.paginator import Paginator
import os

""" the following functions are to control users or admins
    providing some functionality to be used in views
"""


def manager_delete_user(request, id):
    """ delete a specific user not to be able to login and his account is deleted
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        if(user.profile.profile_pic != None):
            delete_profile_pic(user.profile.profile_pic)
        user.delete()
        log(request.user.username+" removed " + user.username+".")
        return HttpResponseRedirect("/manager/users")
    else:
        return HttpResponseRedirect("/")


def manager_show_user(request, id):
    """ show info of specific user all his profile with some additional info only revealed for admins
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        return render(request, "manager/show_user.html", {"user": user})
    else:
        return HttpResponseRedirect("/")


def super_delete_admin(request, id):
    """ delete a specific admin not to be able to login and his account is deleted
    @params : request  , id"""

    current_user = request.user
    if(is_authorized_admin(request)):
        if(current_user.is_superuser):
            user = User.objects.get(pk=id)
            if(user.profile.profile_pic != None):
                delete_profile_pic(user.profile.profile_pic)
            user.delete()
            log(current_user.username+" removed " + user.username+".")
        return HttpResponseRedirect("/manager/admins")
    else:
        return HttpResponseRedirect("/")


def manager_show_admins(request):
    """ show all admin users [admins or super users]
    @params : request """

    if(is_authorized_admin(request)):
        admins = User.objects.filter(is_staff__exact=True)
        paginator = Paginator(admins, 5)
        page_number = request.GET.get('page')
        page_admins = paginator.get_page(page_number)
        context = {"admins": page_admins,
                   "superuser": request.user.is_superuser}
        return render(request, "manager/admins.html", context)
    else:
        return HttpResponseRedirect("/")


def super_lock_admin(request, id):
    """lock a specific admin not to be able to login again but keeping his account and permissions alive
    @params : request  , id"""

    current_user = request.user
    if(is_authorized_admin(request)):
        if(current_user.is_superuser):
            user = User.objects.get(pk=id)
            lock_user(user)
            log(current_user.username+" locked " + user.username+".")
        return HttpResponseRedirect("/manager/admins")
    else:
        return HttpResponseRedirect("/")


def super_unlock_admin(request, id):
    """unlock a specific adminr  to be able to login again
    @params : request  , id"""

    current_user = request.user
    if(is_authorized_admin(request)):
        if(current_user.is_superuser):
            user = User.objects.get(pk=id)
            unlock_user(user)
            log(current_user.username+" unlocked " + user.username+".")
        return HttpResponseRedirect("/manager/admins")
    else:
        return HttpResponseRedirect("/")


def super_demote_admin(request, id):
    """demote  a specific admin to become a normal user again
    @params : request  , id"""

    current_user = request.user
    if(is_authorized_admin(request)):
        if(current_user.is_superuser):
            user = User.objects.get(pk=id)
            demote_user(user)
            log(current_user.username+" demoted " + user.username+".")
        return HttpResponseRedirect("/manager/admins")
    else:
        return HttpResponseRedirect("/")


def manager_promote_user(request, id):
    """promote a specific user to become an admin with all determined permissions
    @params : request  , id"""

    if(is_authorized_admin(request)):
        user = User.objects.get(pk=id)
        promote_to_staff(user)
        log(request.user.username+" promoted " + user.username+".")
        return HttpResponseRedirect("/manager/users")
    else:
        return HttpResponseRedirect("/")


def is_authorized_admin(request):
    if(request.user.is_authenticated):
        if(request.user.is_staff):
            return True
    return False
