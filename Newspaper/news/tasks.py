from datetime import date, timedelta
from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category, Subscription
from accounts.models import CustomUser
from django.core.mail import EmailMultiAlternatives


@shared_task
def weekly_news():
    today = date.today()
    period = today - timedelta(days=7)
    all_posts = Post.objects.filter(create_time__gte=period)
    categories_in_posts = set(all_posts.values_list('category__id', flat=True))
    users = set(Subscription.objects.filter(category__id__in=categories_in_posts).values_list('user', flat=True))

    for user_id in users:
        user = CustomUser.objects.get(id=user_id)
        categories = Category.objects.filter(user=user)
        new_posts = all_posts.filter(category__in=categories)
        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email='mytestemailDilia@yandex.ru',
            to=[user.email],
        )
        html_content = render_to_string(
            'news_for_week.html',
            {
                'posts': new_posts,
                'link': settings.SITE_URL,
                'username': user.username,
            }
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def notify_subscribers(oid):
    post = Post.objects.get(pk=oid)
    categories = post.category.all()
    for item in categories:
        for s in item.user.all():
            msg = EmailMultiAlternatives(
                subject=post.title,
                body='',
                from_email='mytestemailDilia@yandex.ru',
                to=[s.email],
            )
            html_content = render_to_string(
                'news_subscribers.html',
                {
                    'post': post,
                    'link': settings.SITE_URL,
                    'username': s.username,
                }
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
