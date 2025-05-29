from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/', views.event_details, name='event_details'),
    path('<int:event_id>/comment/', views.event_comment, name='event_comment'),
    path('<int:comment_id>/edit/', views.event_edit_comment, name='event_edit_comment'),
    path('<int:comment_id>/delete/', views.event_delete_comment, name='event_delete_comment'),
    path('<int:event_id>/edit/', views.event_update, name='event_update'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('<int:event_id>/participate/', views.participate_in_event, name='participate_in_event'),
    path('<int:event_id>/leave/', views.leave_event, name='leave_event'),
]