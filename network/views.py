from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follower, Post_likes


# a view to display all posts in the home page 
def index(request):
    posts = Post.objects.all().order_by('created_at').reverse()
    posts_ids = posts.values_list('id', flat=True)
    posts_likes = Post_likes.objects.filter(post_id__in=set(posts_ids), user_id=request.user.id)
    paginator = Paginator(posts ,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts_likes' : list(posts_likes.values_list('post_id', flat=True))
        
    }
    return render(request, "network/index.html", context)


# a view for adding posts by user to the blog 
def add_post(request):
    post = Post(content=request.POST['message'], author=request.user)
    post.save()
    return HttpResponseRedirect(reverse("index"))

# update posts in the database
def  update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        post = Post.objects.filter(id=data['msg_id'])[0]
        post.content = data['message']
        post.save()
    return HttpResponse(status=200)

#update the post likes 
def update_post(request):
    current_user = request.user.id
    if request.method  == 'POST':
        data = json.loads(request.body)
        post = Post.objects.filter(id=data['msg_id'])[0]
        post.n_likes = data['n_likes']
        post.save()
        if data['action'] == 'liked':
            post_like = Post_likes(post_id=post, user_id=current_user)
            post_like.save()
        else:
            post_like = Post_likes.objects.filter(post_id=post, user_id=current_user)
            post_like.delete()
    return HttpResponse(status=200)

#update users followers 
def update_follow(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.filter(username=data['username'])[0]
        if data['action'] == 'following':
            follower = Follower(user=user, follower_id=request.user.id)
            follower.save()
        else:
            follower = Follower.objects.filter(user=user, follower_id=request.user.id)
            follower.delete()
    return HttpResponse(status=200)


# a view for displaying all posts from  users who are followed  by the current user 
def follow(request):
    current_user = request.user
    userids = Follower.objects.values_list('follower_id', flat=True).filter(user=current_user.id)
    posts = Post.objects.filter(author__in=set(
        userids)).order_by('created_at').reverse()
    posts_ids = posts.values_list('id', flat=True)
    posts_likes = Post_likes.objects.filter(post_id__in=posts_ids, user_id=current_user.id)
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        'posts_likes': posts_likes.values_list('post_id', flat=True)
    }
    return render(request, "network/folllow.html", context)


# a view to display information about a specific user and his posts.
def profile(request, username):
    userid = User.objects.filter(username=username).first().id
    posts = Post.objects.filter(author=userid).order_by('created_at').reverse()
    posts_ids = posts.values_list('id', flat=True)
    posts_likes = Post_likes.objects.filter(post_id__in=posts_ids, user_id=userid)
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj ,
        "username": username,
        "n_followers":Follower.objects.filter(user=userid).count(),
        "n_following":Follower.objects.filter(follower_id=userid).count(),
        'posts_likes': posts_likes.values_list('post_id', flat=True),
        "is_follower": Follower.objects.filter(user=userid, follower_id=request.user.id)
    }
    return render(request, "network/profile.html", context)


 # The view for logging the user in.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


#The view for logging the user out.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# The view for registering the user in the website.
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

