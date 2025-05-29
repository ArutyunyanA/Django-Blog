from django.urls import path
from . import views

app_name = 'blog'

urlpatterns =[
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_details, name='post_details'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/like/', views.post_like, name='post_like'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/edit/', views.post_edit, name='post_edit'),
    path('search/', views.post_search, name='post_search')
]

"""
Для захвата значений из URL-адреса используются угловые скобки. Любое значение, 
указанное в шаблоне URL-адреса как <parameter>, записывается в качестве строкового литерала. 
Для конкретного сопоставления и возврата целого числа используются конверторы путей, такие как 
<int:year>. Напри- мер, <slug:post> будет, в частности, совпадать со слагом (строковым литералом, 
который может содержать только буквы, цифры, подчеркивания или дефисы).
"""
