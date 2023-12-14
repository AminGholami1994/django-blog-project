from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Article, Comment, Category
from .forms import CommentForm, ArticleForm


def article_list(request):
    articles = Article.objects.all()
    if 'search' in request.GET:
        search = request.GET.get('search')
        articles = articles.filter(Q(title__contains=search) | Q(body__contains=search))
    paginator = Paginator(articles, 2)

    page_numer = request.GET.get("page")
    page_obj = paginator.get_page(page_numer)
    context = {
        'articles': page_obj
    }
    return render(request, 'articles/article_list.html', context=context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        comment_id = request.POST.get('comment_id')

        if form.is_valid():

            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            if comment_id:
                new_comment.parent = Comment.objects.filter(id=comment_id).get()
            new_comment.save()

            return redirect(article)

    form = CommentForm()
    comments = article.comment_set.filter(parent__isnull=True)
    replies = article.comment_set.filter(parent__isnull=False)
    replies_count = article.comment_set.filter(parent__isnull=False).count()

    context = {
        'article': article,
        'form': form,
        'comments': comments,
        'replies': replies,
        'replies_count': replies_count,
    }
    return render(request, 'articles/artile_detail.html', context)


def articles_of_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category_articles = category.article_set.all()
    paginator = Paginator(category_articles, 2)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    context = {
        'articles': articles
    }
    return render(request, 'articles/category_articles.html', context)


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    nex = request.GET.get('next')
    return HttpResponseRedirect(nex)


def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect(article.get_absolute_url())
    form = ArticleForm()
    return render(request, 'articles/create.html', {'form': form})


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'GET':
        form = ArticleForm(instance=article)
        return render(request, 'articles/create.html', {'form': form})

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "The post has been updated successfully.")
            return redirect(article.get_absolute_url())
        else:
            messages.error(request, "Please correct the following errors")
            return render(request, 'articles/create.html', {'form': form})


@login_required
def confirm_delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    context = {
        'article': article
    }
    return render(request, 'articles/confirm_delete.html', context)


def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    messages.success(request, "Your article delete successfully.")
    return redirect('/')


def article_author(request, author):
    articles = Article.objects.filter(author__username=author)
    paginator = Paginator(articles, 2)
    page_number = request.GET.get("page")
    articles = paginator.get_page(page_number)
    context = {
        'articles': articles
    }
    return render(request, 'articles/articles_author.html', context)
