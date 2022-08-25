from django.urls import path
from .views import index, show, LikeView, addComment
    # , likeviewNumber


urlpatterns = [
    path("", index, name="home"),
    path("show", show, name="show"),
    path("like/", LikeView, name="post_like"),
    path("comment/",addComment, name="comment" ),

]


