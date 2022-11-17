from django.urls import path
from profiles.views import profile_edit_view,ChangePasswordView, profile_show_view, Saved_posts

urlpatterns = [
    path("User-profile", profile_edit_view, name="user_profile"),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path("profile-show/<int:id>/", profile_show_view, name="show-profile"),
    path("saved_posts/<int:id>/", Saved_posts, name='saved_posts'),
]