from .models import *


class DataMixin:
    '''Миксин в который вынесен код,
    который формирует контекст для отображения в шаблоне.'''
    
    paginate_by = 10

    def get_user_context_data(self, **kwargs):
        '''Формирует контекст.'''
        
        context = kwargs
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        if 'show_cats' not in context:
            context['show_cats'] = False
        return context
