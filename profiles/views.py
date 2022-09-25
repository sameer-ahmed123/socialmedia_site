from django.shortcuts import render, redirect
from pyexpat.errors import messages
from django.shortcuts import render
from profiles.forms import UpdateProfileForm, UpdateUserForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.


def profile_view(request):
    user_form = UpdateUserForm()
    profile_form = UpdateProfileForm()
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)


        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #messages.success(request, "Profile has been updated successfully")
            return redirect("user_profile")
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, "profiles/profile-page.html", {"user_form": user_form,
                                                          "profile_form": profile_form})



class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'profiles/change-pass.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')