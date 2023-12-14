from .models import Category


def all_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return context
