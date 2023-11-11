from django.shortcuts import render
from django.views.generic import DetailView

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from blog.forms import PostForm
from blog.models import Author, Post

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from community.models import Question
from course.models import Course


def about(request):
    return render(request, 'about.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def index(request):
    tutorials = Course.objects.order_by('-timestamp')[0:3]
    posts = Post.objects.order_by('-timestamp')[0:3]
    questions = Question.objects.order_by('-timestamp')[0:3]

    context = {
        'tutorials': tutorials,
        'posts': posts,
        'questions': questions
    }

    return render(request, 'index.html', context)


def get_author(user):
    lst = Author.objects.filter(id=user.id)
    return lst[0] if lst else None

def paginate_objects(request, queryset, num):
    paginator = Paginator(queryset, num)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return queryset


def get_posts(request):
    posts = Post.objects.order_by('-timestamp')

    search_request_var = 'q'
    search_query = request.GET.get(search_request_var, '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(overview__icontains=search_query)
        ).distinct()

    posts = paginate_objects(request, posts, 5)

    context = {
        'posts': posts,
        'page_request_var': 'page',
        'search_request_var': search_request_var,
        'search_query': search_query,
    }

    return render(request, 'blog/posts.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


def create_post(request):
    form = PostForm(request.POST, request.FILES or None)
    context = {"form": form}
    author = get_author(request.user)

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to ask a request to create a post."
    elif not request.user.is_staff:
        context["authority_error"] = "Bad Request: You are not authorized to create a blog post."
    elif not author:
        context["authority_error"] = "Bad Request: You are not given permission to create/edit/delete a blog post."
    else:
        if request.method == "POST":
            if form.is_valid():
                form.instance.author = author
                post = form.save()
                return redirect(reverse("post_detail", kwargs={
                    'pk': form.instance.pk,
                    'slug': post.slug
                }))
            else:
                context["error"] = form.errors

    return render(request, 'blog/post_create.html', context)


def update_post(request, pk, slug):
    obj = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, instance=obj)
    context = {"form": form}
    author = get_author(request.user)

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to ask a request to edit a post."
    elif not request.user.is_staff:
        context["authority_error"] = "Bad Request: You are not authorized to create/edit/delete a blog post."
    elif not author:
        context["authority_error"] = "Bad Request: You are not given permission to create/edit/delete a blog post."
    elif request.user != obj.author.user:
        context["authority_error"] = "Bad Request: Blog post belongs to another user. Thus, you are not " \
                                     "allowed to edit this post."
    else:
        if request.method == "POST":
            if form.is_valid():
                post = form.save()
                return redirect(reverse("post_detail", kwargs={
                    'pk': form.instance.pk,
                    'slug': post.slug
                }))
            else:
                context["error"] = form.errors

    return render(request, 'blog/post_update.html', context)


def delete_post(request, pk, slug):
    post = get_object_or_404(Post, id=pk)
    author = get_author(request.user)
    context = {
        "post": post
    }

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to ask a request to delete a post."
    elif not request.user.is_staff:
        context["authority_error"] = "Bad Request: You are not authorized to create/edit/delete a blog post."
    elif not author:
        context["authority_error"] = "Bad Request: You are not given permission to create/edit/delete a blog post."
    elif request.user != post.author.user:
        context["authority_error"] = "Bad Request: Blog post belongs to another user. Thus, you are not " \
                                     "allowed to delete this post."
    else:
        if request.method == "POST":
            post.delete()
            return redirect(reverse("questions"))

    return render(request, 'blog/post_delete.html', context)
