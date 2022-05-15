from django.shortcuts import render
from .models import Post, Tag, Category, Comment, Profanity
from django.core.paginator import  Paginator
from users.logger import log
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from posts.forms import PostForm, CommentForm
from users.util_funcs import delete_profile_pic
from users.logger import log
from django.db.models import Q

# Create your views here.



def posts(request):
    posts = Post.objects.all()
    popular_posts = Post.objects.order_by('-likes')[:5]
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Category.objects.all()
    tags = Tag.objects.all()[:10]
    user = request.user

    context = {'page_obj': page_obj, 'categories': categotries,
               'tags': tags, 'user': user, 'popular_posts': popular_posts}
    return render(request, 'home.html', context)

########################## create post #######################
def createPost(request):
    student_form = PostForm()
    if request.method == 'POST':
        student_form = PostForm(request.POST, request.FILES)
    if student_form.is_valid():
            post = student_form.save(commit=False)
            post.user = request.user
            tag_list = getTags(request.POST.get('post_tags'))
            post.save()
            queryset = Tag.objects.filter(name__in=tag_list)
            post.tags.set(queryset)
            return HttpResponseRedirect('/')
    else:
        context = {"student_form": student_form}
        return render(request, "form_post.html", context)

########################## tags #######################
def getTags(string):
    tag_list = list(string.split(" "))
    for tag in tag_list:
        if not Tag.objects.filter(name=tag):
            Tag.objects.create(name=tag)
    return tag_list 


def post_detail(request, id):
    categotries = Category.objects.all()
    tags = Tag.objects.all()[:10]
    post = Post.objects.get(id=id)
    user = request.user
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    profane_words = Profanity.objects.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            for profane_word in profane_words:
                if str(profane_word) in content:
                    user.profile.undesired_words_count += 1
                    user.profile.save()
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            Comment.objects.create(
                post=post, user=request.user, content=content, reply=comment_qs)
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categotries,
        'tags': tags,
        'user': user
    }
    return render(request, 'single.html', context)

########################## update post #######################
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            img = request.FILES.get('image')
            if (img):
                if(post.image):
                    delete_profile_pic(post.image)
                post.image = img
            post.user = request.user
            tag_list = getTags(request.POST.get('post_tags'))
            post.save()
            queryset = Tag.objects.filter(name__in=tag_list)
            post.tags.set(queryset)
            return HttpResponseRedirect('/')
    else:
        form = PostForm(instance=post)
        context = {"pt_form": form}
        return render(request, "edit_post.html", context)    

########################## delete post #######################
def post_delete(request, num):
    instance = Post.objects.get(id=num)
    instance.delete()
    return HttpResponseRedirect('/')


def subscribe(request, cat_id):
    user = request.user
    category = Category.objects.get(id=cat_id)
    category.user.add(user)
    # send email to user after subscription
    try:
        send_mail("subscribed to a new category", 'hello ,'+user.first_name+" "+user.last_name+'\nyou have just subscribed to category '+category.name,
                  'dproject.os40@gmail.com', [user.email], fail_silently=False,)
    except Exception as ex:
        log("couldn't send email message"+str(ex))
    return HttpResponseRedirect('/')  


def unsubscribe(request, cat_id):
    user = request.user
    category = Category.objects.get(id=cat_id)
    category.user.remove(user)
    return HttpResponseRedirect('/')
       

########################## searche by category#######################
def categoryPosts(request, cat_id):
    category = Category.objects.get(id=cat_id)
    posts = Post.objects.filter(category=category)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Category.objects.all()
    tags = Tag.objects.all()[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'home.html', context)

####################search by tag name################
def tagPosts(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    posts = tag.post_set.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Category.objects.all()
    tags = Tag.objects.all()[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'home.html', context)

#################### search button in sidebar action ##################
def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query))
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Category.objects.all()
    tags = Tag.objects.filter(Q(name__icontains=query))[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'home.html', context)
############### delete comment in post ######################
def commentDelete(request, post_id, com_id):
    comment = Comment.objects.get(id=com_id)
    comment.delete()
    return HttpResponseRedirect('/post/'+post_id)
############ edit commint in posts #########################
def commentEdit(request, post_id,com_id):
    comment = Comment.objects.get(id=com_id)
    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES, instance=comment )
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect('/')
    else:
        form = CommentForm(instance=comment)
        return render(request, 'edit_comment.html', {'form': form})
        
