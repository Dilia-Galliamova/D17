from django.urls import path
from .views import PostsList, ArticleCreate, ArticleUpdate, ArticleDelete, upgrade_me, OnePost, PostsFilter, subscribe

from django.views.decorators.cache import cache_page


urlpatterns = [
   path('search/', PostsFilter.as_view(), name='post_search'),
   path('create/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>', OnePost.as_view(), name='one_post'),
   path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('search/subscribe/<int>', subscribe, name='subscribe')
]
