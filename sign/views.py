from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.contrib.auth.models import User
from news.models import Author, Category, SubscribedUsersCategory
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group



class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    if not Author.objects.filter(authorUser=user).exists():
        Author.objects.create(authorUser=user)
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')

def unsubscribe(request):
    user = request.user
    category_id = request.GET.get('category_id')
    category = Category.objects.get(id=category_id)
    if category.subscribed.filter(email=request.user.email).exists():
        SubscribedUsersCategory.objects.filter(subscribed=user, category=category).delete()

    return redirect('/')






