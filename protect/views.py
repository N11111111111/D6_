from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import *
from django.contrib.auth.models import User
from news.models import Author, Category, SubscribedUsersCategory
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


    def get_object(self, **kwargs):
        username = self.request.user.username
        return User.objects.get(username=username)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        context['user_category'] = Category.objects.filter(subscribed=self.request.user)
        return context


# @login_required
# def unsubscribe(request):
#     user = request.user
#     category_id = request.GET.get('category_id')
#     category = Category.objects.get(id=category_id)
#     if category.subscribed.filter(email=request.user.email).exists():
#         SubscribedUsersCategory.objects.filter(subscribed=user, category=category).delete()
#
#     return redirect('/')