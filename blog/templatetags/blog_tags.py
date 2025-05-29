from django import template
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.db.models import Count
from blog.models import Comment
from django import template
from ..models import Post
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

register = template.Library()
User = get_user_model()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.simple_tag
def get_user_following(user, count=5):
    return user.followers.all()[:count]

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.simple_tag
def get_most_liked_posts(count=5):
    return Post.published.annotate(total_likes=Count('likes')).order_by('-total_likes')[:count]

@register.filter
def get_comment(comments, comment_id):
   return next((c for c in comments if c.id == int(comment_id)), None)

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['fenced_code', CodeHiliteExtension(linenums=True)]))
