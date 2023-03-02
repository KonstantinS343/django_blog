from django.shortcuts import redirect,render
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout, login
import transliterate

from BLOG.utils import DataMixin
from .forms import *
from .models import *

class RegisterUser(DataMixin, generic.CreateView):
    '''Класс для регистрации пользователя на сайте.'''
    
    template_name = 'users/register.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        '''Формирует контекст для передачи его шаблону.'''
        
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context_data(title='Регистрация')
        return dict(list(context.items()) + list(user_context.items()))
    
    def form_valid(self, form):
        '''После регистрации пользователя совершает
        вход в аккаунт и перенаправляет на главную страницу.'''
        
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class LoginUser(DataMixin, LoginView):
    '''Класс для входа пользователя в аккаунт.'''
    
    template_name = 'users/login.html'
    form_class = UserLogin
    
    def get_context_data(self, **kwargs):
        '''Формирует контекст для передачи его шаблону.'''
        
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context_data(title='Авторизация')
        return dict(list(context.items()) + list(user_context.items()))
    
    def get_success_url(self):
        '''При успешном входе перенаправляет на главную страницу.'''
        
        return reverse_lazy('home')
    
def user_logout(request):
    '''Реализует выход пользователя из аккаунта.'''
    
    logout(request)
    return redirect('home')

def user_profile(request,slug):
    '''Функция отображает профиль пользователя,
    а также содержит формы для обновления данных пользователя.'''
    
    if request.method == 'POST':
        form_for_data = UserUpdateForm(request.POST, instance=request.user)
        form_for_image = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if form_for_data.is_valid() and form_for_image.is_valid():
            form_for_image.save()
            form_for_data.save()
            try:
                user_slug = Profile.objects.get(user = request.user)
            except BaseException:
                raise Http404()
            return redirect('profile',user_slug.slug)
    else:
        form_for_data = UserUpdateForm(instance=request.user)
        form_for_image = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form_for_data':form_for_data,
        'form_for_image':form_for_image,
    }

    return render(request,'users/profile.html',context)
       

# Create your views here.
