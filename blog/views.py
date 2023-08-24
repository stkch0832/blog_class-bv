from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Article
from .forms import ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator

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
        return render(request, 'blog/article_detail.html', context= {
            'article_data': article_data,
        })


class ArticleEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article_data = Article.objects.get(id=self.kwargs['pk'])
        form = ArticleForm(
            request.POST or None,
            initial={
                'title':article_data.title,
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
