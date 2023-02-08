from datetime import datetime

from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from accounts.models import CustomUser

post = 'PS'
news = 'NW'

POST_TYPE = [(post, 'Статья'), (news, 'Новость')]


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text=_('category name'))

    user = models.ManyToManyField(CustomUser, through='Subscription')

    def __str__(self):
        return f'{self.name}'


class Author(models.Model):
    rating = models.FloatField(default=0.0)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def update_rating(self):
        s1 = self.post_set.aggregate(s=Sum('rating')*3)['s']
        s2 = self.user.comment_set.aggregate(s=Sum('rating'))['s']
        s3 = self.post_set.aggregate(s=Sum('comment__rating'))['s']
        self.rating = s1 + s3 + s2
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=datetime.now, blank=True)
    type = models.CharField(max_length=2, choices=POST_TYPE)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(
        Category,
        through='PostCategory',
    )

    def __str__(self):
        return self.text[:10]

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return reverse('one_post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
