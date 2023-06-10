import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Category, Post, Comment

from .forms import PostForm, CommentForm, UserForm

from blog.mixins import DispatchDetailMixin

NUMBER = 10


def post_filter():
    """ Фильтр для отбора постов. """
    time_now = datetime.datetime.now()
    return Post.objects.select_related(
        'location', 'category', 'author'
    ).filter(
        pub_date__lte=time_now,
        is_published=True,
        category__is_published=True,
    )


def paginator_page_obj(request, posts):
    """ Пагинатор. """
    paginator = Paginator(posts, NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
def index(request):
    """ Главная страница проекта. """
    template = 'blog/index.html'
    post_list = (
        post_filter()
        .order_by('-pub_date')
        .annotate(comment_count=Count('comments'))
    )
    page_obj = paginator_page_obj(request, post_list)
    context = {'page_obj': page_obj}
    return render(request, template, context)


@login_required
def post_detail(request, id):
    """ Страница отдельной публикации. """
    template = 'blog/detail.html'
    post_list = get_object_or_404(
        post_filter(),
        pk=id,
    )
    comments = post_list.comments.all()
    context = {
        'post': post_list,
        'form': CommentForm(),
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def category_posts(request, category_slug):
    """ Страница категории. """
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(slug=category_slug), is_published=True
    )
    post_list = (post_filter().order_by('-pub_date').filter(
        category=category).annotate(comment_count=Count('comments'))
    )
    page_obj = paginator_page_obj(request, post_list)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_profile(request, username_slug):
    """ Страница пользователя."""
    template = 'blog/profile.html'
    user = get_object_or_404(
        User.objects.filter(username=username_slug)
    )
    post_list = Post.objects.filter(
        author=user.id).order_by(
        '-pub_date').annotate(comment_count=Count('comments'))
    page_obj = paginator_page_obj(request, post_list)
    context = {
        'profile': user,
        'page_obj': page_obj,
    }
    return render(request, template, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """ Добавления постов."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        slug = self.request.user.username
        return reverse('blog:profile', kwargs={'username_slug': slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView, DispatchDetailMixin):
    """ Редактирование постов. """
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """ Обновление профиля пользователя. """
    model = User
    template_name = 'blog/user.html'
    form_class = UserForm
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    """ Создания комментария. """

    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs['pk']}
        )


class CommentUpdateView(LoginRequiredMixin, UpdateView, DispatchDetailMixin):
    """ Редактирование комментария. """
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs['post_id']}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView, DispatchDetailMixin):
    """ Удаление поста. """
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = {'instance': self.object}
        return context


class CommentDeleteView(LoginRequiredMixin, DeleteView, DispatchDetailMixin):
    """ Удаление комментария. """
    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')
