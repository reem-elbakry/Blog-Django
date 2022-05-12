from django.shortcuts import render
from .crud_users import *

# Create your views here.


def index(request):
    return render(request, 'manager/index.html')


def admins(request):
    return manager_show_admins(request)


def show(request, id):
    return manager_show_user(request, id)


def delete(request, id):
    return manager_delete_user(request, id)


def delete_admin(request, id):
    return super_delete_admin(request, id)


def lock_admin(request, id):
    return super_lock_admin(request, id)


def unlock_admin(request, id):
    return super_unlock_admin(request, id)


def demote(request, id):
    return super_demote_admin(request, id)


def promote(request, id):
    return manager_promote_user(request, id)
