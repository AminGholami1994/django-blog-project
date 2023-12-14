from django import forms
from django.forms import Textarea
from .models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': Textarea(attrs={'cols': 80, 'rows': 4, 'class': 'form-control',
                                    'placeholder': 'Comment here !', 'id': 'body'})
        }

        labels = {
           'body': ''
        }


class ArticleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild in self.visible_fields():
            fild.field.widget.attrs['class'] = 'block border border-gray-600 rounded'

    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'category']
