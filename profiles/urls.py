from django.urls import path
from profiles.views import profile_view,ChangePasswordView



urlpatterns = [
    path("User-profile", profile_view, name="user_profile"),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]