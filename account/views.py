from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact, CustomUser
from event.models import Event, EventParticipant
from blog.models import Post
import logging


logger = logging.getLogger(__name__)
User = get_user_model()
"""
[X] Излишний код ни на что не влияет, так как настроена под класс аутентификации из коробки,
[X] На удаление

@login_required
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Перенаправляем пользователя в dashboard после успешного логина
                    return redirect('account:dashboard')  # Убедитесь, что имя URL 'dashboard' правильное
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
"""

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            try:
                Profile.objects.create(user=new_user)
                logger.info(f"Profile created for user {new_user.id}")
            except Exception as e:
                logger.error(f"Failed to create profile for user {new_user.id}: {e}")

            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section': 'people', 'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    is_following = Contact.objects.filter(user_from=request.user, user_to=user).exists()
    followers_count = Contact.objects.filter(user_to=user).count()
    return render(request, 'account/user/detail.html', {
        'section': 'people', 
        'user': user, 
        'is_following': is_following,
        'followers_count': followers_count
        })


@login_required
def user_follow(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        action = request.POST.get('action')
        user = get_object_or_404(CustomUser, id=user_id)

        if action == "follow":
            Contact.objects.get_or_create(user_from=request.user, user_to=user)
        elif action == "unfollow":
            Contact.objects.filter(user_from=request.user, user_to=user).delete()
        request.user.refresh_from_db()
        return redirect("account:user_detail", username=user.username)
    return JsonResponse({"status": "error"})
    

@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    followers = user.following_by_set.all()
    return render(request, 'account/user/followers_list.html', {'user': user, 'followers': followers})

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    profile = get_object_or_404(Profile, user=request.user)
    created_events = Event.objects.filter(creator=request.user)
    participant_events = Event.objects.filter(participants__user=request.user)
    return render(request, 'account/dashboard.html', {
        'section': 'dashboard', 
        'posts': posts, 
        'profile': profile,
        'created_events': created_events,
        'participant_events': participant_events
        })

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

