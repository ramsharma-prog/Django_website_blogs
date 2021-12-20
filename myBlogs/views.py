from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Post, Comment
from . import forms
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)


from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


# NOT IN USE
class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key_index'] = ' Please follow the links above'
        return context


class AboutView(TemplateView):
    """ This is an about class for company info """
    template_name = 'myBlogs/about.html'


class PostListView(ListView):
    """ This class will get all the objects through the get_queryset function
    which will be published by date thriugh timezone """

    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
       return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    """ This class will return the detail of the post with given promary key
    inside the urls.py """
    model = Post
    template_name = 'myBlogs/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = 'myBlogs/post_detail.html'
    form_class = forms.PostForm
    model = Post
    template_name = 'post_form.html'


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'myBlogs/post_detail.html'
    form_class = forms.PostForm
    model = Post
    template_name = 'myBlogs/post_form.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class PostDraftView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'myBlogs/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

# ----------------------------------------------------#


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

###############################################################################
###############################################################################


@login_required
def add_comment_to_post(request, pk):
    """ To attach comments to the post"""
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = forms.CommentForm()

    return render(request, 'myBlogs/comment_form.html', context={'form': form})


@login_required
def comment_approve(request, pk):
    """ To approve comments """
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
