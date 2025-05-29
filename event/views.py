from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, EventParticipant, Comment
from .forms import EventCreateForm, EventCommentForm
from django.contrib.auth.decorators import login_required

def event_list(request):
    events = Event.objects.all()
    city = request.GET.get('city')
    date = request.GET.get('date')

    if city:
        events = events.filter(city__iexact=city)
    if date:
        events = events.filter(date=date)
    events = events.order_by('date', 'time')
    return render(request, 'event/event_list.html', {'events': events})

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participants.select_related('user')
    participants_ids = participants.values_list('user_id', flat=True)
    # Загружаем комментарии с сортировкой по дате
    comments = event.comments.filter(active=True).select_related('author').prefetch_related('replies').order_by('created')
    
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

    form = EventCommentForm()
    return render(request, 'event/event_details.html', {
        'event': event, 
        'participants': participants, 
        'participants_ids': participants_ids,
        'form': form,
        'comments': root_comments,
        })

@login_required
def event_comment(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user

            parent_id = request.POST.get('parent')
            if parent_id:  # Проверяем, передан ли parent_id
                try:
                    parent_comment = Comment.objects.get(id=int(parent_id), event=event)
                except (Comment.DoesNotExist, ValueError):
                    parent_comment = None  # Если комментарий не найден, делаем его корневым
                comment.parent = parent_comment

            comment.save()
            return redirect(event.get_absolute_url() + f"#comment-{comment.id}")

    return redirect(event.get_absolute_url())

@login_required
def event_edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == "POST":
        form = EventCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.event.get_absolute_url() + f"#comment-{comment.id}")
    else:
        form = EventCommentForm(instance=comment)

    return render(request, 'event/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def event_delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == "POST":
        post_url = comment.event.get_absolute_url()
        comment.delete()
        messages.success(request, "Your comment has been deleted.")
        return redirect(post_url)

    return render(request, 'event/delete_comment.html', {'comment': comment})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('event:event_list')
    else:
        form = EventCreateForm()
    return render(request, 'event/event_create.html', {'form': form})

@login_required
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.creator != request.user:
        raise PermissionDenied("You don not have a permission to edit this event!")
    if request.method == 'POST':
        form = EventCreateForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event:event_details', event_id=event.id)
    else:
        form = EventCreateForm(instance=event)
    return render(request, 'event/event_update.html', {'form': form, 'event': event})

@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.creator != request.user:
        raise PermissionDenied("You don not have a permission to delete this event!")
    if request.method == 'POST':
        event.delete()
        return redirect('event:event_list')
    return render(request, 'event/event_delete.html', {'event': event})

@login_required
def participate_in_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participant, created = EventParticipant.objects.get_or_create(user=request.user, event=event)
    if not created:
        participant.delete()
    else:
        participant.save()
    return redirect('event:event_details', event_id=event.id)

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participant = EventParticipant.objects.filter(user=request.user, event=event).first()
    if participant:
        participant.delete()
    return redirect('event:event_details', event_id=event.id)
