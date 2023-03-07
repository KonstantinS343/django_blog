from django.shortcuts import render
from django.http import HttpResponseNotFound, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import F
from django.urls import reverse_lazy
from django.views import generic

from .models import *
from .forms import *
from .utils import *


class HomeView(DataMixin, generic.ListView):
    '''Отображает главную страницу со списком последних постов.'''
    
    model = Question
    template_name = 'BLOG/index.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Формирует контекст для передачи его шаблону.'''
        
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context_data(show_cats=True)
        return dict(list(context.items()) + list(user_context.items()))
    
    def get_queryset(self):
        '''Формирует список для отображения.'''
        
        try:
            return Question.objects.select_related('cat').select_related('author_post')
        except BaseException:
            raise Http404()

def about(request):
    '''Отображает страницу с информацией о сайте.'''
    
    return render(request, 'BLOG/about.html', {'title': 'О нас'})


class Categories(DataMixin, generic.ListView):
    '''Производит фильтрацию постов по определенной категории.'''
    
    model = Question
    template_name = 'BLOG/index.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Формирует контекст для передачи его шаблону.'''
        
        context = super().get_context_data(**kwargs)

        try:
            user_context = self.get_user_context_data(
                cat_selected=context['post'][0].cat_id,
                title=context['post'][0].cat,
                show_cats=True)
        except BaseException:
            raise Http404()
        return dict(list(context.items()) + list(user_context.items()))

    def get_queryset(self):
        '''Формирует список для отображения.'''
        
        try:
            return Question.objects.filter(cat_id=self.kwargs['cat_id']).select_related('cat').select_related('author_post')
        except BaseException:
            raise Http404()


class ShowPost(LoginRequiredMixin, DataMixin, generic.DetailView):
    '''Показывает детальную информацию о посте.
    Доступно только авторизированным пользователям.'''
    
    model = Question
    template_name = 'BLOG/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        '''Формирует контекст для передачи его шаблону.'''
        
        context = super().get_context_data(**kwargs)

        try:
            user_context = self.get_user_context_data(
                cat_selected=context['post'].cat_id,
                title=context['post'].title,
                show_cats=True)
        except BaseException:
            raise Http404()
        context['post'].add_views(context['post'], self.request)
        return dict(list(context.items()) + list(user_context.items()))


class AddPost(LoginRequiredMixin, DataMixin, generic.CreateView):
    '''Отображает форму для добавления поста.
    Доступно только авторизированным пользователям.'''
    
    form_class = AddNewPost
    template_name = 'BLOG/addpost.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        '''Формирует контекст для передачи его шаблону.'''
        
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context_data(
            title='Добавить задачу', change_or_add='Добавить')
        return dict(list(context.items()) + list(user_context.items()))

    def form_valid(self, form):
        '''Сохраняет информацию о авторе поста.'''
        
        form.instance.author_post = self.request.user
        return super().form_valid(form)


class Search(DataMixin, generic.ListView):
    '''Отображает результаты поиска.'''
    
    template_name = 'BLOG/index.html'
    model = Question
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Формирует контекст для передачи его шаблону.'''
        
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context_data(show_cats=True)
        return dict(list(context.items()) + list(user_context.items()))

    def get_queryset(self):
        '''Формирует список для отображения.'''
        
        return Question.objects.filter(
            title__contains=self.request.GET.get('search')).select_related('cat')


class UpdatePost(UserPassesTestMixin, generic.UpdateView):
    '''Реализует форму для обновления информации в посте.
    Доступно только авторизированным пользователям.'''
    
    model = Question
    fields = ['title', 'content', 'cat']

    def form_valid(self, form):
        '''Сохраняет информацию о авторе поста.'''
        
        form.instance.author_post = self.request.user
        return super().form_valid(form)

    def test_func(self):
        '''Проверка является ли авторизированный пользователь автором поста.'''
        
        post = self.get_object()
        return post.author_post == self.request.user


class DeletePost(UserPassesTestMixin, generic.DeleteView):
    '''Реализует форму для удаления поста.
    Доступно только авторизированным пользователям.'''
    
    model = Question
    success_url = '/'

    def test_func(self):
        '''Проверка является ли авторизированный пользователь автором поста.'''

        post = self.get_object()
        return post.author_post == self.request.user


class UserPosts(DataMixin, generic.ListView):
    '''Отражает посты конкретного пользователя.'''
    models = Question
    template_name = 'BLOG/index.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Формирует контекст для передачи его шаблону.'''
        
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context_data()
        return dict(list(context.items()) + list(user_context.items()))

    def get_queryset(self):
        '''Формирует список для отображения.'''
        return Question.objects.filter(author_post=self.request.user).select_related('cat').select_related('author_post')


def PageNotFound(request, exception):
    '''Вызывает ошибка, если такой страницы не существует.'''
    
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# Create your views here.
