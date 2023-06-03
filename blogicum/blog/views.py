from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post

NUMBER_OF_POSTS = 5


def index(request):
    """Главная страница проекта"""

    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:NUMBER_OF_POSTS]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    """Страница отдельной публикации"""

    template = 'blog/detail.html'
    post_list = get_object_or_404(
        Post.objects.select_related(
            'location', 'author', 'category'
        ).filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ),
        pk=id,
    )
    context = {'post': post_list}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Страница категории"""

    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category=category
    ).order_by('-pub_date',)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
