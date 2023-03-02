from django import template
from django.db.models import Count
from django.http import Http404

from BLOG.models import *
from users.models import *
register = template.Library()

@register.inclusion_tag('BLOG/choice_list.html')
def show_categories(cat_selected):
    '''Пользовательский тег для отображения меню выбора категорий.'''
    
    cats = Categories.objects.order_by('name').annotate(Count('question'))
    return {'cats':cats, 'cat_selected':cat_selected}

@register.simple_tag()
def get_user(user):
    '''Пользовательский тег, который возвращает информацию о пользователе.'''
    
    try:
        return Profile.objects.get(user = user)
    except BaseException:
        raise Http404()
    
    


        
         