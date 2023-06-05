from django.db import models
import string
import random
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils import timezone

User = get_user_model()

validate_comma_separated_integer_list = models.CommaSeparatedIntegerField(default=0000)

def generate_unique_no():
  length = 10

  while True:
    acc_number = ''.join(random.choices(string.digits ,k=length))
    if Accounts.objects.filter(acc_number=acc_number).count() == 0:
      break

  return acc_number
# Create your models here.
class Accounts(models.Model):
  user_main = models.ForeignKey(User, on_delete=models.CASCADE)
  acc_number = models.CharField(max_length=10, default=generate_unique_no, unique=True)
  phone_no = models.CharField(max_length=11, blank=True)
  phone_no2 = models.CharField(max_length=11, blank=True)
  phone_no3 = models.CharField(max_length=11, blank=True)
  transaction_pin = models.CharField(max_length=5, default=00000, blank=False)
  first_name = models.CharField(max_length=30, blank=False)
  middle_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=30, blank=False)
  acc_balance = models.FloatField(blank=True, default=0000.00)
  profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

  def __str__(self):
      return self.acc_number
  


class Deposit(models.Model):
  acc = models.ForeignKey(Accounts, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  amount = models.FloatField(blank=False, default=0.00)
  transaction_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)


class Withdraw(models.Model):
  acc = models.ForeignKey(Accounts, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  amount = models.FloatField(blank=False, default=0.00)
  transaction_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)


class Send(models.Model):
  sender = models.CharField(max_length=100)
  description = models.CharField(max_length=1000, blank=True)
  receiver = models.CharField(max_length=100)
  date = models.DateTimeField(auto_now_add=True)
  amount = models.FloatField(blank=False, default=0.00)
  transaction_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)


class SaveRecipient(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  acc = models.ForeignKey(Accounts, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)


class Receipts(models.Model):
  saved_receipt = models.CharField(max_length=1000)
  transaction_type = models.CharField(max_length=30, blank=False, default='receipt')
  acc = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)


class SearchRec(models.Model):
  query = models.CharField(max_length=1000)
  acc = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)


'''
#Chatting
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
        hours = '{:02d}:{:02d} pm'.format(self.time_sent.hour, self.time_sent.minute)
    else:
        hours = '{:02d}:{:02d} am'.format(self.time_sent.hour, self.time_sent.minute)

    return hours '''