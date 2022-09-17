from django.urls import path
from .views import index, create_post, show, LikeView,getComments, login_view, delete_post,post_comment,edit_post,Purge,logout_view

urlpatterns = [
    path("logout/",logout_view, name="logout_view" ),
    path("login", login_view, name="login_view" ),
    path("", index, name="home"),
    path("show", show, name="show"),
    path("like/", LikeView, name="post_like"),
    path("comment/<int:id>/", getComments, name="post_detail" ),
    path("comment/<int:id>/post", post_comment, name="post-comment"),
    path("create-post", create_post, name="create-post"),
    path("edit-post/<int:id>/", edit_post, name="edit_post"),
    path("post-delete<int:id>/", delete_post ,name="post_delete"),
    path("purge", Purge, name="purge"),
]


