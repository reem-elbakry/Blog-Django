from django.shortcuts import render
from .crud_users import *
from posts.models import Post, Category, Profanity
# from posts.forms import PostForm, CommentForm, ProfanityForm, CategoryForm

# Create your views here.


def index(request):
    return render(request, 'manager/index.html')


def users(request):
    return manager_show_normal_users(request)


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


def lock(request, id):
    return manager_lock_user(request, id)


def unlock(request, id):
    return manager_unlock_user(request, id)


def posts(request):
    if(is_authorized_admin(request)):
        posts = Post.objects.all()
        categories = Category.objects.all()
        profane_words = Profanity.objects.all()
        context = {'posts': posts, 'categories': categories,
                   'profane_words': profane_words}
        return render(request, 'manager/landing.html', context)
    else:
        return HttpResponseRedirect("/")
