from django.forms import ModelForm, widgets, ModelChoiceField, CharField, Select, DateTimeField, ModelMultipleChoiceField, Textarea
from django.forms import ModelForm
from .models import *


class PostForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all(), label='Автор:')

    category = ModelMultipleChoiceField(label='Категория', queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categoryType',   'category']












