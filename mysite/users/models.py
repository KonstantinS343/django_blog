#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
import transliterate


class Profile(models.Model):
    '''Модель пользовательского профиля.'''
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/%Y/%m/%d/')
    slug = models.SlugField(
        db_index=True,
        max_length=255,
        unique=True,
        null=True,
        verbose_name='url') 

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        '''Формирует slug, который используется
        для формирования url адреса.'''
        
        try:
            create_slug = transliterate.translit(self.user.username, reversed=True)
        except:
            create_slug = self.user.username
        self.slug = slugify(create_slug)
        super().save(*args, **kwargs)
        self.save_img(self,args,kwargs)
        
    def save_img(self, *args, **kwargs):
        '''Сжимает изображение профиля.'''
        
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

