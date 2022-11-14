from multiprocessing import context
from django.shortcuts import render, redirect
from pyexpat.errors import messages
from django.shortcuts import render
from profiles.forms import UpdateProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from profiles.models import Profile
from app.models import Posts
from django.http import JsonResponse,HttpResponseRedirect
from django.core import serializers

# Create your views here.


def profile_edit_view(request):
    #user_form = UpdateUserForm()
    profile_form = UpdateProfileForm()
    if request.method == "POST":
       # user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if  profile_form.is_valid():
            profile_form.save()
            #messages.success(request, "Profile has been updated successfully")
            return redirect("user_profile")
        else:
           # user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, "profiles/profile-page.html", {
                                                          "profile_form": profile_form})


def profile_show_view(request, id):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()
    
    profile = Profile.objects.get(id=id)
    posts = Posts.objects.filter(user=profile.user)
    
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    
    following_count = Profile.following_count(self=profile)
    
    context = {
        "profile": profile,
        "posts": posts,
        "following_count":following_count,
    }
    return render(request , "profiles/profilePage.html", context)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'profiles/change-pass.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')
    
    
def Saved_posts(request, id):
    #favorites__in=user_profile.favorites.all()
    user = request.user
    profile = Profile.objects.get(id=id)
    # user_profile =Profile.objects.get(user=user)
    saved_posts = Profile.objects.filter(user=user)
    #saved_posts = serializers.serialize("json", Posts.objects.filter(user=user))
    
    
    
    #after serializing , the unserialized obect , now im getting un defined in the template
    
    
    
    
    context = {
        "profile": profile,
        "saved_posts": saved_posts,
    }
    # return HttpResponseRedirect('/saved_posts')
    #return JsonResponse(context)

    return render(request, "profiles/saved_posts.html", context)