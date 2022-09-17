from email import message
from pyexpat.errors import messages
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from app.forms import login_form, postCreateForm, CommentForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy, reverse
from .models import Posts, Comments
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

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
    return render(request, "authentication/logout.html")

def login_view(request):
    form = login_form
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
        "form": form
    }
    return render(request, "authentication/login.html", context)


def show(request, *args, **kwargs):
    try:
        obj = Posts.objects.all()
    except:
        return HttpResponse("No Posts Found !!!")

    context = {
        "obj": obj,
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
            result = post.like_count
            like_unlike = "like"
            class_state = "btn-outline-success "
            class_rm = "btn-outline-danger"
            post.save()
        else:
            post.like.add(request.user)
            post.like_count += 1
            result = post.like_count
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