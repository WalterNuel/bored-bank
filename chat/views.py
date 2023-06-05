from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from django.http import HttpResponse

from bank.models import *

from .models import *

def room_make(userA, userB):
  rooms = ChatRoom.objects.create(userA=userA, userB=userB)
  rooms.save()
  acc = User.objects.get(username=userA)

  rooms = ChatRoom.objects.get(userA=userA, userB=userB)

  room_chat = ChatMsg.objects.create(home=rooms, text_body=f"Message on Bored", msg_type='alert', acc=acc, name='user')

  return rooms.id


# Create your views here.
def chat(request, pk):
  chatView ='n'
  rooms = ChatRoom.objects.all()

  for i in rooms:
    if i.userA == request.user.username and i.userB == pk:
      chatView = 'y'
      return redirect(f'/messages/{i.id}')
    elif i.userB == request.user.username and i.userA == pk:
      chatView = 'y'
      return redirect(f'/messages/{i.id}')
  
  if chatView != 'y':
    room_make(request.user.username, pk)
    room = ChatRoom.objects.get(userA=request.user.username, userB=pk)

    return redirect(f'/messages/{room.id}')

  return HttpResponse(f'<h1>{request.user.username}:{pk}</h1>') 


def message_home(request):
  my_acc = User.objects.get(username=request.user.username)
  rooms = ChatRoom.objects.all().order_by('-active_date')
  my_rooms = []

  for i in rooms:
    if i.userA == request.user.username or i.userB == request.user.username:
      my_rooms.append(i)

  chats = ChatMsg.objects.filter(acc=my_acc)
  my_chats = []

  for i in my_rooms:
    recent = ChatMsg.objects.filter(home=i).latest('time_sent')
    if recent:
      my_chats.append(recent)


  context = {
    'rooms':my_rooms,
    'chats':my_chats,
    'my_acc':my_acc
  }

  return render(request, 'messaging.html', context)


def message_page(request, uuid):
  chat = ChatRoom.objects.get(id=uuid)
  chat_msg = ChatMsg.objects.filter(home=chat)
  all_type = 'text'

  current_user = request.user.username

  sending_user = ''
  sending_profile = ''

  receiving_user = ''
  receiving_profile = ''

  if chat.userA == current_user or chat.userB == current_user:
    if chat.userA == current_user:
      sending_user = User.objects.get(username=chat.userA)
      sending_profile = Accounts.objects.get(user_main=sending_user)

      receiving_user = User.objects.get(username=chat.userB)
      receiving_profile = Accounts.objects.get(user_main = receiving_user)

    elif chat.userB == current_user:
      sending_user = User.objects.get(username=chat.userB)
      sending_profile = Accounts.objects.get(user_main=sending_user)

      receiving_user = User.objects.get(username=chat.userA)
      receiving_profile = Accounts.objects.get(user_main = receiving_user)

  context = {
    'chat':chat,
    'user':sending_user,
    'receiver':receiving_user,
    'user_acc':sending_profile,
    'receiver_acc':receiving_profile,
    'msg':chat_msg,
    'type':all_type
  }

  return render(request, 'message-page.html', context)


def msg_upload(request, uuid):
  user = User.objects.get(username=request.user.username)
  user_acc = Accounts.objects.get(user_main=user)

  if request.method == 'POST':
    home = ChatRoom.objects.get(id=uuid)
    text_body = request.POST['text_body']
    acc = user
    msg_type = 'text'
    name = request.user.username
    profile_img = user_acc.profile_img

    if text_body == '':
      return redirect(f'/messages/{uuid}')

    new_msg = ChatMsg.objects.create(home=home, text_body=text_body, acc=acc, name=name, msg_type=msg_type)
    room_date = home
    room_date.active_date = new_msg.time_sent
    room_date.save()
    new_msg.save()
    return redirect(f'/messages/{uuid}')