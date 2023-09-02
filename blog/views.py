from datetime import date
from typing import Any, Dict
from django.db.models.query import QuerySet

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm

class StartingPageView(ListView):
  template_name = "blog/index.html"
  model = Post
  ordering = ["-date"]
  context_object_name = "posts"
  
  def get_queryset(self):
    queryset = super().get_queryset()
    data = queryset[:3]
    
    return data

all_posts = [
]

def get_date(post):
  return post["date"]

# Create your views here.

def starting_page(request):
  latest_posts = Post.objects.all().order_by("-date")[:3] # order by desc order
  # sorted_posts = sorted(all_posts, key=get_date)
  # latest_posts = sorted_posts[-3:]
  return render(request, "blog/index.html", {
    "posts": latest_posts
  })
  
class AllPostsView(ListView):
  template_name = "blog/all-posts.html"
  model = Post
  ordering = ["-date"]
  context_object_name = "all_posts"
  
class SinglePostView(View):
  # template_name = "blog/post-detail.html"
  # model = Post
  
  # def get_context_data(self, **kwargs: Any):
  #   context = super().get_context_data(**kwargs)
  #   context["post_tags"] = self.object.tags.all()
  #   context["comment_form"] = CommentForm()
    
  #   return context
  
  def get(self, request, slug):
    post = Post.objects.get(slug=slug)
    context = {
      "post": post,
      "post_tags": post.tags.all(),
      "comment_form": CommentForm()
    }
    
    return render(request, "blog/post-detail.html", context=context)
    
  def post(self, request, slug):
    post = Post.objects.get(slug=slug)
    comment_form = CommentForm(request.POST)
    
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.post = post
      comment.save()
      
      return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
    
    context = {
      "post": post,
      "post_tags": post.tags.all(),
      "comment_form": comment_form
    }
    
    return render(request, "blog/post-detail.html", context=context)

def posts(request):
  all_posts = Post.objects.all().order_by("-date")
  return render(request, "blog/all-posts.html", {
    "all_posts": all_posts
  })

def post_detail(request, slug):
  identified_post = get_object_or_404(Post, slug=slug)

  return render(request, "blog/post-detail.html", {
    "post": identified_post,
    "post_tags": identified_post.tags.all()
  })
