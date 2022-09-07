from django.urls import path
from .views import index, show, LikeView,getComments, login_view

#  logout_view,
urlpatterns = [
    # path("logout/",logout_view, name="logout_view" ),
    path("login", login_view, name="login_view" ),
    path("", index, name="home"),
    path("show", show, name="show"),
    path("like/", LikeView, name="post_like"),
    path("show/<int:id>/", getComments, name="post_detail" ),
    
]


