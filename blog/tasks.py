from celery import shared_task
from django.utils import timezone
from .models import Post

@shared_task
def update_post_dates():
    posts = Post.objects.all()
    for post in posts:
        post.date = timezone.now()
        post.save()
    return f"Updated {len(posts)} posts"