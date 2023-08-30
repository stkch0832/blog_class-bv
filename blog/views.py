from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Article, Category, Comment
from .forms import ArticleForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from functools import reduce
from operator import and_

class IndexView(View):
    def get(self, request, *args, **kwargs):
        article_data = Article.objects.select_related('author__profile').all().order_by('-id')

        paginator = Paginator(article_data, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/index.html', context= {
            'page_obj': page_obj,
            })


class ArticleCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm(request.POST or None)

        return render(request, 'blog/article_form.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = ArticleForm(
            request.POST or None,
            request.FILES or None,
            )

        if form.is_valid():
            article_data = Article()
            article_data.author = request.user
            article_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            article_data.category = category_data
            article_data.content = form.cleaned_data['content']
            article_data.image = form.cleaned_data['image']
            article_data.save()
            messages.success(request, '新規投稿が完了しました')
            return redirect('blog:index')

        return render(request, 'blog/article_form.html', context={
            'form': form
        })


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        article_data = Article.objects.select_related('author__profile').get(id=self.kwargs['pk'])
        comment_data = Comment.objects.filter(article_id=self.kwargs['pk']).order_by('-id')
        form = CommentForm(request.POST or None)

        return render(request, 'blog/article_detail.html', context= {
            'article_data': article_data,
            'comment_data': comment_data,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST or None)
        article_data = Article.objects.get(id=self.kwargs['pk'])
        comment_data = Comment.objects.fetch_by_article_id(self.kwargs['pk'])

        if comment_form.is_valid():
            comment = Comment()
            comment.comment = comment_form.cleaned_data['comment']
            comment.article_id = self.kwargs['pk']
            comment.user_id = request.user
            comment.save()
            return redirect('blog:article_detail', article_data.id)

        return render(request, 'blog/article_detail.html', context={
            'form': comment_form,
            'article_data': article_data,
            'comment_data': comment_data,
        })

    # def delete_comment(self, request, *args, **kwargs):
    #     comment_data = Comment.objects.get(id=self.kwargs['comment_id'])
    #     comment_data.delete()
    #     return redirect('blog:article_detail')


class ArticleEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article_data = Article.objects.get(id=self.kwargs['pk'])
        form = ArticleForm(
            request.POST or None,
            initial={
                'title':article_data.title,
                'category': article_data.category,
                'content':article_data.content,
                'image':article_data.image,
                'created_at':article_data.created_at,
            }
        )

        return render(request, 'blog/article_form.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = ArticleForm(
            request.POST or None,
            request.FILES or None,
            )

        if form.is_valid():
            article_data = Article.objects.get(id=self.kwargs['pk'])
            article_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_date = Category.objects.get(name=category)
            article_data.category = category_date
            article_data.content = form.cleaned_data['content']
            article_data.image = form.cleaned_data['image']
            article_data.save()
            messages.success(request, '内容変更が完了しました')
            return redirect('blog:article_detail', self.kwargs['pk'])

        return render(request, 'blog/article_form.html', context={
            'form': form
        })

class ArticleDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article_data = Article.objects.get(id=self.kwargs['pk'])
        article_data.delete()
        messages.success(request, '投稿削除が完了しました')
        return redirect('blog:index')


class CommentDelete(View):
    def post(self, request, *args, **kwargs):
        comment_data = Comment.objects.get(id=self.kwargs['comment_id'])
        comment_data.delete()
        return redirect('blog:article_detail', pk=self.kwargs['pk'])


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        article_data = Article.objects.order_by('-id').filter(category=category_data)
        return render(request, 'blog/index.html', context={
            'article_data': article_data,
        })


class SearchView(View):
    def get(self, request, *args, **kwargs):
        article_data = Article.objects.order_by('-id')
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set([' ', '　'])
            query_list = ''
            for word in keyword:
                if not word in exclusion_list:
                    query_list += word
            query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in query_list])
            article_data = article_data.filter(query)

        return render(request, 'blog/index.html', context={
            'keyword': keyword,
            'page_obj': article_data,
        })
