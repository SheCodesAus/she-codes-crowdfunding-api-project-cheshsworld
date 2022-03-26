from django.contrib.auth.models import AbstractUser
from django.contrib.auth import  get_user_model
from django.db import models
from django.dispatch import receiver

User = get_user_model

class CustomUser(AbstractUser):
    profile_image = models.URLField(null = True, blank = True)
    bio = models.TextField(max_length=200, null = True)
    banner_image = models.URLField(null = True, blank = True)
    following = models.ManyToManyField('CustomUser', related_name='followers')        

    def __str__(self):
        return self.username


class Message(models.Model):
    receiver = models.ForeignKey(
        'CustomUser', 
        on_delete = models.SET_NULL,
        null= True,
        blank = True,      
        related_name='receivers'
    )
    sender = models.ForeignKey(
        get_user_model(),   
        on_delete = models.SET_NULL,
        null= True,
        blank = True,    
        related_name='senders'
    )
    sent_at = models.DateField()
    read_at = models.DateField(null = True)
    body = models.TextField()


