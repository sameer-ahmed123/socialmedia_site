from ast import arg
from email import message
import profile
from pyexpat.errors import messages
from turtle import pos
from typing_extensions import Self
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from app.forms import login_form, postCreateForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy, reverse
from .models import Posts, Comments
from profiles.models import Profile
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from profiles.models import Profile # used for user profile image

# Create your views here.


@login_required
def index(request):
    obj = Posts.objects.all()
    context = {
        "obj": obj
    }

    return render(request, "posts/index.html", context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return render(request, "account/logout.html")


def login_view(request):
    form = login_form
    User = get_user_model()
    users = User.objects.all()[:5]
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)                    
                    
        if user is not None:
            login(request, user)
            print(user)
            return JsonResponse({
                "status": "user logged in , Redirecting",
              })
        else:
            return JsonResponse({
                "status": "Invalid Credentials",
              })

    context = {
        "form": form,
        "users": users
    }
    return render(request, "account/login.html", context)


def register_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend="django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            messages.success(request, "Registration Complete")
            return redirect("home")
        else:
            messages.error(request, "Unsuccessful Registration , please try again")
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {"form":form})

def show(request, *args, **kwargs):
    try:
        obj = Posts.objects.all()
        profile = Profile.objects.all()
        
        
    except:
        return HttpResponse("No Posts Found !!!")
    
    context = {
        "obj": obj,
        "profile": profile
        
    }

    return render(request, "posts/show.html", context)

@csrf_exempt
def LikeView(request):
    if request.POST.get('action') == 'post':
        result = ''
        class_state = ''
        like_unlike = ''
        class_rm = ''
        id = request.POST.get('postid')
        
        post = get_object_or_404(Posts, id=id)
        if request.user in post.like.all():
            post.like.remove(request.user)
            post.like_count -= 1
            numerized = post.like_formatted()
            result = numerized
            like_unlike = "like"
            class_state = "btn-outline-success "
            class_rm = "btn-outline-danger"
            post.save()
        else:
            post.like.add(request.user)
            post.like_count += 1
            numerized = post.like_formatted()
            result = numerized
            # result = post.like_count
            like_unlike = "Unlike"
            class_state = "btn-outline-danger "
            class_rm = "btn-outline-success"
            post.save()

        context = {
            'result': result,
            "like_unlike": like_unlike,
            'class_state': class_state,
            "class_rm": class_rm
        }

        return JsonResponse(context)

def getComments(request, id):
    the_comments = Posts.objects.get(id=id)
    context = {
        "comments": the_comments
    }
    return render(request, "posts/comments/comments_show.html", context)

def post_comment(request,id):
    result = ''
    comments_id = request.POST.get("comments_id")
    print("comments id is ", comments_id)
    the_comments = Posts.objects.get(id=id)
    comment = request.POST.get("comment")

    context = {
        "comments": the_comments,
    }
    data = {
        "result": result
    }
    if request.htmx:
        if request.method == "POST":
            comnt = Comments(comment=comment, user=request.user, post=the_comments)
            comnt.save()
        print("htmx comment")
        return render(request, "posts/comments/comment_partial.html", context)
    return render(request, "posts/comments/comments_show.html", context)

def delete_post(request, id):
    post = get_object_or_404(Posts, id=id)
    context = {
        "post": post
    }
    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(request, "posts/delete_post.html", context)


@login_required
def create_post(request):
    form = postCreateForm
    if request.method == "POST":
        form = postCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            print("saving")
            return redirect("home")
    else:
        form = postCreateForm()
        print("not saving")

    context = {
        "form": form
    }
    return render(request, "posts/create_post.html", context)


def edit_post(request, id):
    post = get_object_or_404(Posts, id=id, user=request.user)
    print(str(post))
    form = postCreateForm(request.POST or None,request.FILES or None, instance=post)
    
    if form.is_valid():
        form.save()
        print("saving")
        return redirect("home")
    context = {
        "form": form,
        "post": post
    }
    return render(request, "posts/edit_post.html", context)

def Purge(request):
    post = Posts.objects.all()
    post.delete()
    return render(request, "posts/index.html", {"post":post})

@login_required
def favourite_posts(request):
    status = ""
    remove_icon_state = ""
    icon_state = ""
    user = request.user
    if request.POST.get('action') == 'post':
        id = request.POST.get('save_postid')
        user_profile =Profile.objects.get(user=user) 
        post = get_object_or_404(Posts, id=id)

        if user_profile.favorites.filter(id=id).exists():
            user_profile.favorites.remove(post)
            status = "add"
            remove_icon_state = "fa-solid fa-bookmark"
            icon_state = "fa-regular fa-bookmark"
        else:   
            user_profile.favorites.add(post)
            status = "remove"
            remove_icon_state = "fa-regular fa-bookmark"
            icon_state = "fa-solid fa-bookmark"
       
        context = {
            "status": status,
            "id": id,
            "icon_state": icon_state,
            "remove_icon_state": remove_icon_state
        }

    return JsonResponse(context)
    