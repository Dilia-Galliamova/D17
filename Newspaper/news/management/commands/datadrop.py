from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Delete all posts from category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **kwargs):
        category = Category.objects.get(name=kwargs['category'])
        self.stdout.write(f'Вы правда хотите удалить все статьи в категории {category}? yes/no')
        answer = input()

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                Post.objects.filter(category == category).delete()
                self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {category}'))