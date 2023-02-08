from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Post, PostCategory, Subscription
from django.template.loader import render_to_string


# @receiver(m2m_changed, sender=PostCategory)
# def notify_subscribers(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         for item in categories:
#             for s in item.user.all():
#                 msg = EmailMultiAlternatives(
#                     subject=instance.title,
#                     body='',
#                     from_email='mytestemailDilia@yandex.ru',
#                     to=[s.email],
#                 )
#                 html_content = render_to_string(
#                     'news_subscribers.html',
#                     {
#                         'post': instance,
#                         'link': settings.SITE_URL,
#                         'username': s.username,
#                     }
#                 )
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()
