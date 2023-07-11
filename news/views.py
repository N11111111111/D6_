from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect



#главная страница
class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    gueryset = Post.objects.order_by('-id')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()

        return context



#найти новость или статью, фильтрация, пагинация

class SearchPosts(ListView):
    paginate_by = 3
    model = Post
    ordering = '-dateCreation'
    template_name = 'post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


#подробности о статье или новости:
class PostDetail(DetailView):
    model = Post
    template_name = 'id.news.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_category'] = Category.objects.filter(subscribed=self.request.user)
        else:
            context['user_category'] = None
        return context


# создаем:

class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm
    context_object_name = 'post_create'
    success_url = '/news/'
    login_url=reverse_lazy('login')
    permission_required = ('news.add_post')
    # raise_exception = True


# удаляем
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all
    success_url = '/news/'

    login_url = reverse_lazy('login')
    permission_required = ('news.delete_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

# редактируем
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    context_object_name = 'post_edit'
    success_url = '/news/'
    login_url = reverse_lazy('login')
    permission_required = ('news.change_post')

def subscription(request):
    category_id = request.GET.get('category_id')
    category = Category.objects.get(id=category_id)
    if not category.subscribed.filter(email=request.user.email).exists():
        user = request.user
        SubscribedUsersCategory.objects.create(subscribed=user, category=category)
    return redirect('/')













