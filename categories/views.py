from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.text import slugify

from articles.models import Category
from categories.forms import CategoryForm


def categories(request):

    category_list = Category.objects.all()
    context = {
        'categories': category_list
    }
    return render(request, 'categories/category_list.html', context)


@login_required
def create_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(form.cleaned_data['title'])
            category.save()
            return redirect('category_list')

    return render(request, 'categories/create.html', {'form': form})
