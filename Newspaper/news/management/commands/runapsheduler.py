# import logging
# from datetime import datetime, date, timedelta
#
# from django.conf import settings
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.core.mail import EmailMultiAlternatives
# from django.core.management.base import BaseCommand
# from django.template.loader import render_to_string
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
#
# from news.models import Post, Category, Subscription
#
# from accounts.models import CustomUser
#
# logger = logging.getLogger(__name__)
#
#
# # наша задача
# def my_job():
#     today = date.today()
#     period = today - timedelta(days=7)
#     all_posts = Post.objects.filter(create_time__gte=period)
#     categories_in_posts = set(all_posts.values_list('category__id', flat=True))
#     users = set(Subscription.objects.filter(category__id__in=categories_in_posts).values_list('user', flat=True))
#
#     for user_id in users:
#         user = CustomUser.objects.get(id=user_id)
#         categories = Category.objects.filter(user=user)
#         new_posts = all_posts.filter(category__in=categories)
#         msg = EmailMultiAlternatives(
#             subject='Статьи за неделю',
#             body='',
#             from_email='mytestemailDilia@yandex.ru',
#             to=[user.email],
#         )
#         html_content = render_to_string(
#             'news_for_week.html',
#             {
#                 'posts': new_posts,
#                 'link': settings.SITE_URL,
#                 'username': user.username,
#             }
#         )
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#
#
#
# # функция, которая будет удалять неактуальные задачи
# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs apscheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         # добавляем работу нашему задачнику
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"), #day_of_week="mon", hour="00", minute="00"
#             # То же, что и интервал, но задача тригера таким образом более понятна django
#             id="my_job",  # уникальный айди
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info(
#             "Added weekly job: 'delete_old_job_executions'."
#         )
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")