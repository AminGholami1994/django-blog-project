from django.urls import path
from . import views


urlpatterns = [
    path('', views.article_list, name="article_list"),
    path('<int:article_id>/', views.article_detail, name="article_detail"),
    path('<str:slug>/articles', views.articles_of_category, name="category-articles"),
    path('delete-comment/<int:comment_id>', views.delete_comment, name="delete-comment"),
    path('create/', views.create_article, name="create_article"),
    path('edit/<int:article_id>/', views.edit_article, name="edit_article"),
    path('delete/<int:article_id>/', views.delete_article, name="delete_article"),
    path('delete/<int:article_id>/confirm/', views.confirm_delete_article, name='confirm_delete_article'),

    path('<str:author>/articles/', views.article_author, name="article_author"),
]
