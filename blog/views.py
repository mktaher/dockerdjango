from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden

# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'home.html'

class Article(DetailView):
    model = Post
    template_name = 'article.html'

class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'addpost.html'
    fields = ['title', 'body']  # Exclude the 'author' field from the form

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != '2027mtaher':
            return HttpResponseForbidden("You are not authorized to add posts.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Automatically set the logged-in user as the author of the post
        form.instance.author = self.request.user
        return super().form_valid(form)