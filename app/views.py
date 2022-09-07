from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from app.forms import login_form, postCreateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from .models import Posts, Comments
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    obj = Posts.objects.all()
    if request.method == "POST":
        logout(request)
        return redirect("login_view")
    context = {
        "obj": obj
    }

    return render(request, "index.html", context)

# def logout_view(request):
#     if request.method == "POST":
#         logout(request)
#         return redirect("home")
#     return render(request, "logout.html")


def login_view(request):
    form = login_form
    if request.method == "POST":
        form = login_form(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("logedin as", user)
            return redirect("home")
    else:
        form = login_form(request)
    context = {
        "form": form
    }
    return render(request, "login.html", context)


def show(request, *args, **kwargs):
    try:
        obj = Posts.objects.all()
    except:
        return HttpResponse("No Posts Found !!!")

    context = {
        "obj": obj,
    }

    return render(request, "show.html", context)


@csrf_exempt
def LikeView(request):
    if request.POST.get('action') == 'post':
        result = ''
        like_unlike = ''
        id = request.POST.get('postid')
        post = get_object_or_404(Posts, id=id)
        if request.user in post.like.all():
            post.like.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            like_unlike = "like"
            post.save()
        else:
            post.like.add(request.user)
            post.like_count += 1
            result = post.like_count
            like_unlike = "Unlike"
            post.save()

        return JsonResponse({'result': result, "like_unlike": like_unlike})


def getComments(request, id):
    the_comments = Posts.objects.get(id=id)
    comment = request.POST.get("comment")
    print(str(the_comments))
    if request.method == "POST":
        comnt = Comments(comment=comment, user=request.user, post=the_comments)
        comnt.save()
    if request.htmx:
        print("htmx comment")
        return render(request, "comments.html")
    return render(request, "comments_show.html", {"comments": the_comments})

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
    return render(request, "create_post.html", context)
