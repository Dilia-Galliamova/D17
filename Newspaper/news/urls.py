from django.urls import path
from .views import PostsList, OnePost, PostCreate, PostUpdate, PostDelete, PostsFilter, \
   upgrade_me, subscribe

from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', cache_page(60)(PostsList.as_view()), name='posts'),
   path('search/', PostsFilter.as_view(), name='post_search'),
   path('<int:pk>', OnePost.as_view(), name='one_post'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('search/subscribe/<int>', subscribe, name='subscribe'),
]
