from django import forms

from .models import *


class AddNewPost(forms.ModelForm):
    '''Форма для создания нового поста.'''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбраны'

    class Meta:
        model = Question
        fields = ['title', 'content', 'cat']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': 5,
                    'cols': 60,
                    'class': 'content-input',
                    'placeholder': 'Дано два числа...'}),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Название'}),
            'cat': forms.Select(
                attrs={
                    'class': 'cat-choice'})}
