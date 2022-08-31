from django.urls import path
from .views import index, show, LikeView,getComments, logout_view


urlpatterns = [
    path("", index, name="home"),
    path("show", show, name="show"),
    path("like/", LikeView, name="post_like"),
    path("show/<int:id>/", getComments, name="post_detail" ),
    path("logout/",logout_view, name="logout_view" ),
]


