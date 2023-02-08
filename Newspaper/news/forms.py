from django import forms
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError

from .models import Post, Author, Category
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):

    class Meta:
       model = Post
       fields = ['title', 'text', 'category', 'author']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
