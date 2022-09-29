from django.urls import path
from profiles.views import profile_view,ChangePasswordView, profile_show_view



urlpatterns = [
    path("User-profile", profile_view, name="user_profile"),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path("profile-show/<int:id>/", profile_show_view, name="show-profile"),
]