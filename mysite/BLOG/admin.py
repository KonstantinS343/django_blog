from django.contrib import admin

from .models import *


class QuestionAdmin(admin.ModelAdmin):
    '''Отображает информацию о модели Question в админ панели.'''
    
    list_display = (
        'id',
        'title',
        'pub_date',
        'author_post',
        'views',
        'cat',
        'slug')
    search_fields = ('id', 'title')
    list_display_links = ('title', 'id', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['who_see_post']


class CategoriesAdmin(admin.ModelAdmin):
    '''Отображает модель Categories в админ панели.'''
    
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Categories, CategoriesAdmin)

# Register your models here.
