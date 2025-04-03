from django.urls import path
from . views import HomeView, Article, AddPost

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('article/<int:pk>', Article.as_view(), name="article"),
    path('addpost/', AddPost.as_view(), name="addpost"),
]