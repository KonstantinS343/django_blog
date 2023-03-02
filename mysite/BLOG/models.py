from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import F
from django.contrib.auth.models import User

import transliterate
import time
import random
import string

from users.models import Profile

class Question(models.Model):
    '''Модель для реализации поста.'''
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(
        db_index=True,
        max_length=255,
        unique=True,
        null=True,
        verbose_name='url')
    content = models.TextField(verbose_name='Содержание')
    author_post = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')
    views = models.IntegerField(
        verbose_name='Количество просмотров', default=0)
    cat = models.ForeignKey(
        'Categories',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Категория')
    who_see_post = models.ManyToManyField(Profile)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        '''Формирует slug, который используется
        для формирования url адреса.'''
        
        if not self.slug:
            try:
                create_slug = transliterate.translit(self.title, reversed=True) + str(int(time.time())) + ''.join(
                    [random.choice(string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase) for i in range(10)])
            except BaseException:
                create_slug = self.title + str(int(time.time()))
            self.slug = slugify(create_slug)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        '''Формирует адрес до конкретного поста.'''
        
        return reverse("post", kwargs={"post_slug": self.slug})

    def get_views(self):
        '''Определяет отображение большого количества просмотров.'''
        
        if self.views // 1000000 >= 1:
            return str(round(self.views / 1000000, 2)) + 'М'
        elif self.views // 1000 >= 1:
            return str(round(self.views / 1000, 2)) + 'K'
        else:
            return str(self.views)
        
    def add_views(self, context, request):
        '''Реализует обновление количества просмотров поста.'''
        
        user_try_open_post = Profile.objects.get(user = request.user)
        if user_try_open_post not in context.who_see_post.all():
            context.views = F('views') + 1
            context.who_see_post.add(user_try_open_post)
            context.save()
            context.refresh_from_db()


    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ["-pub_date", "title"]


class Categories(models.Model):
    '''Определяет модель категорий постов.'''
    
    name = models.CharField(
        db_index=True,
        max_length=20,
        verbose_name='Категория')

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        '''Формирует адрес для отображения постов конкретной категории.'''
        
        return reverse("categories", kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
