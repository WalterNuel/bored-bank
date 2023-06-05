import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from bank.models import *


# Create your models here.
class ChatRoom(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  userA = models.CharField(max_length=100)
  userB = models.CharField(max_length=100)
  active_date = models.DateTimeField(auto_now_add=True)


class ChatMsg(models.Model):
  home = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  text_body = models.TextField()
  msg_type = models.CharField(default='text', blank=False, max_length=30)
  acc = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=30, default='user', null=False)
  time_sent = models.DateTimeField(auto_now_add=True)

  def time(self):
    check = self.time_sent.day
    ago = timezone.now() - self.time_sent

    if self.time_sent.hour > 12:
        hours = '{}:{:02d} pm'.format(self.time_sent.hour, self.time_sent.minute)
    else:
        hours = '{}:{:02d} am'.format(self.time_sent.hour, self.time_sent.minute)

    return hours


  # def time_length(self):
  #   check = self.time_sent.day
  #   ago = timezone.now() - self.time_sent
    
  #   if ago.days < 1:
  #     if self.time_sent.hour > 12:
  #         hours = '{}:{:02d}  PM'.format(self.time_sent.hour, self.time_sent.minute)
  #     else:
  #         hours = '{}:{:02d}  AM'.format(self.time_sent.hour, self.time_sent.minute)

  #   elif ago.days == 1:
  #     hours = 'Yesterday'

  #   elif ago.days > 1:
  #     hours = f'{self.time_sent.day}/{self.time_sent.month}'

  #   return hours

  def time_length(self):
    hours = timezone.now() - self.time_sent

    if hours.days == 1:
      hours = 'Yesterday'  

    elif hours.days > 7:
      hours = hours.days // 7
      hours = f'{hours}w'

    elif hours.days == 7:
      hours = 1
      hours = f'{hours}w'

    elif hours.days < 0 or hours.days == 0:
      hours = hours.seconds // 60
      if hours == 60 or hours > 60:
        hours = hours // 60
        hours = f'{hours}h'
      else:
        if 5 > hours:
          hours = 'Just Now'
        else:
          hours = f'{hours}m'
        
    else:
      hours = f'{hours.days}d'
       
    return hours