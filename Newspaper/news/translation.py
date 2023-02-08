from .models import Category, Post, Comment
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Post)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('title', 'text', 'type')


@register(Comment)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('text',)
