from django.shortcuts import render
from .crud_users import *

# Create your views here.


def index(request):
    return render(request, 'index.html')


def admins(request):
    return manager_show_admins(request)


def show(request, id):
    return manager_show_user(request, id)


def delete(request, id):
    return manager_delete_user(request, id)
