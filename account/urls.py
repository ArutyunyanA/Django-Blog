from django.urls import path, include 
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    #path('login/', views.user_login, name='login'),

    # url-адреса входа/выхода
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # url-адреса смены пароля
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url='/account/password-change/done/'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    # url-адреса сброса пароля
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='/account/password-reset/done/'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/account/password-reset/complete/'), name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('user/', views.user_list, name='user_list'),
    path('user/follow/', views.user_follow, name='user_follow'),
    path('user/<username>/', views.user_detail, name='user_detail'),
    path('user/<username>/followers/', views.followers_list, name='followers_list')
    ]

