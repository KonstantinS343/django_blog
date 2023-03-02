from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender = User)
def create_user(instance,created,**kwargs):
    '''Сигнал для создания поля в Profile,
    которое связано с базовой таблицей User.'''
    
    if created:
        Profile.objects.create(user = instance)
    
    