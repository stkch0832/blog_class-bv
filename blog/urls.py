from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/new/', views.ArticleCreateView.as_view(), name='article_new'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/edit/', views.ArticleEditView.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),

    path('article/<int:pk>/<int:comment_id>/delete/', views.CommentDelete.as_view(), name='comment_delete'),

    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('search/', views.SearchView.as_view(), name='search'),

]
