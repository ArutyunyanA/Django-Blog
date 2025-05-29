from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib import messages
from django.utils.text import slugify
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .forms import EmailPostForm, CommentForm, SearchForm, PostForm
from taggit.models import Tag
from .models import Post, Comment, Like, Category




def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    category_slug = request.GET.get('category')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    if category_slug:
        post_list = post_list.filter(category__slug=category_slug)

    categories = Category.objects.all()

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {
        'posts': posts,
        'tag': tag,
        'categories': categories,
    })



@login_required
def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
    # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s commments: {cd['comments']}"
            send_mail(subject, message, 'your@accountmail.com', [cd['to']])
            sent = True
    # ... отправить электронное письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_details(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    is_like = post.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    like_count = post.likes.count()

    # Загружаем комментарии с сортировкой по дате
    comments = post.comments.filter(active=True).select_related('parent').order_by('created')
    
    # Формируем дерево комментариев
    comment_dict = {comment.id: comment for comment in comments}
    root_comments = []

    for comment in comments:
        if comment.parent_id:
            parent = comment_dict.get(comment.parent_id)
            if parent:
                parent.replies_list = getattr(parent, 'replies_list', [])
                parent.replies_list.append(comment)
        else:
            root_comments.append(comment)

    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]

    return render(
        request,
        'blog/post/details.html',
        {
            'post': post,
            'comments': root_comments,  # Теперь только корневые комментарии
            'form': form,
            'similar_posts': similar_posts,
            'is_like': is_like,
            'like_count': like_count
        }
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Добавил request.FILES для загрузки изображения
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if not post.slug:
                post.slug = slugify(post.title)  # Генерация slug, если его нет
            post.save()
            return redirect(post.get_absolute_url())

    else:
        form = PostForm()

    return render(request, 'blog/post/post_create.html', {'form': form})

@login_required
def post_edit(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)

    if request.user != post.author:
        return redirect(post.get_absolute_url())

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post/post_edit.html', {'form': form, 'post': post})


@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            parent_id = request.POST.get('parent')
            if parent_id:  # Проверяем, передан ли parent_id
                try:
                    parent_comment = Comment.objects.get(id=int(parent_id), post=post)
                except (Comment.DoesNotExist, ValueError):
                    parent_comment = None  # Если комментарий не найден, делаем его корневым
                comment.parent = parent_comment

            comment.save()
            return redirect(post.get_absolute_url() + f"#comment-{comment.id}")

    return redirect(post.get_absolute_url())


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.post.get_absolute_url() + f"#comment-{comment.id}")
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/post/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == "POST":
        post_url = comment.post.get_absolute_url()
        comment.delete()
        messages.success(request, "Your comment has been deleted.")
        return redirect(post_url)

    return render(request, 'blog/post/delete_comment.html', {'comment': comment})



@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post)
    if like.exists():
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)
    return redirect("blog:post_details", year=post.publish.year, month=post.publish.month, day=post.publish.day, post=post.slug)