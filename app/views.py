from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy,reverse
from .models import Posts, Comments
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    form = AuthenticationForm
    obj = Posts.objects.all()
    context = {
        "form": form,
        "obj": obj
    }
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
    if request.htmx:
        return render(request, "login-form.html", context)

    return render(request, "index.html", context)


def show(request, *args, **kwargs):
    try:
        obj = Posts.objects.all()
    except:
        return HttpResponse("No Posts Found !!!")


    context = {
        "obj": obj,
    }


    return render(request, "show.html", context)


def LikeView(request, ):
    post_like = get_object_or_404(Posts, id=request.POST.get("post_id") )


    if request.user in post_like.like.all():
        post_like.like.remove(request.user)
    else:
        post_like.like.add(request.user)

    if request.htmx:
        return render(request, "like_page.html", )  #abhi htmx k through me likes kar raha hu hay hay maze
    return HttpResponseRedirect(reverse("home"))

def likeviewNumber(request, *args,**kwargs):#this needs to be resolved
    the_id = request.GET.get('liked_post_')  #this needs to be resolved
    print("the id",the_id) #this needs to be resolved
    liked_post = get_object_or_404(Posts,id=1)      #this needs to be resolved
    print(liked_post)
    context = {
        "liked_post":liked_post
    }

    if request.htmx:
        return render(request,"like_counting.html", context)
    return render(request,"like_counting.html", context)
# HttpResponseRedirect(reverse( "show", args=[ str(id) ]) )


def addComment(request):
    comment = request.POST.get("comment")
    # post_id = request.POST.get("comment_post_id")
    post = get_object_or_404(Posts, id=request.POST.get("comment_post_id"))

    if request.method == "POST":
        comnt = Comments(comment=comment, user=request.user, post=post)
        comnt.save()
    if request.htmx:
        return render(request, "comments.html")
    return render(request, "index.html")


# def GetComments(request):
