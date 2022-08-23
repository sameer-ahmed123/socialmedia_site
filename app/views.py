from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy,reverse
from .models import Posts, Comments
from django.http import HttpResponseRedirect, JsonResponse
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




def LikeView(request):
    if request.POST.get('action') == 'post':
            # post_id = request.POST.get('post_id')
            result = ''
            id = request.POST.get('postid')
            post = get_object_or_404(Posts, id=id)
            if request.user in post.like.all():
                post.like.remove(request.user)
                post.like_count -= 1
                result = post.like_count
                post.save()
            else:
                post.like.add(request.user)
                post.like_count += 1
                result = post.like_count
                post.save()

            return JsonResponse({'result': result})

    # if request.POST.get('action') == 'POST':
    #     result = ""
    #     id = request.POST.get('postid')
    #     post = get_object_or_404(Posts,id)
    #     if post.like.filter(id=request.user.id).exists():
    #         post.like.remove(request.user)
    #         post.like_count -= 1
    #         result = post.like_count
    #         post.save()
    #     else:
    #         post.like.add(request.user)
    #         post.like_count += 1
    #         result = post.like_count
    #         post.save()
    #
    #     return JsonResponse({"result": result})


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
