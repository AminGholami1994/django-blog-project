from django.forms import ModelForm

from articles.models import Category


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['title', 'description']