from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from chat.models import *
from chat.views import room_make

from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='signin')
def HomePage(request):
  user = User.objects.get(username=request.user.username)
  acc = Accounts.objects.get(user_main=user)

  amount = acc.acc_balance
  cash = '{:,.2f}'.format(amount)

  acc_change = acc.acc_number
  acc_change = acc_change[0:3] + 'XXXX' + acc_change[7:10]

  favorites = SaveRecipient.objects.filter(user=user)
  len_of_fav = len(favorites)
  if len_of_fav > 3:
    favorites = favorites[0:4]
  else:
    pass

  context = {
    'cash':cash,
    'current_user':acc,
    'acc_no':acc_change,
    'favs':favorites,
    'no_favs':len_of_fav
  }

  return render(request, 'index.html', context)


def signup(request):
  if request.method == 'POST':
    username = request.POST['username']
    first_name = request.POST['first_name']
    middle_name = request.POST['mid_name']
    last_name = request.POST['last_name']
    phone_no = request.POST['phone_number']
    password = request.POST['password']
    password2 = request.POST['password2']

    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.info(request, 'Username Taken')
        return redirect('signup')
      else:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.save()

        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)

        user_model = User.objects.get(username=username)
        new_acc = Accounts.objects.create(user_main=user_model, first_name=first_name, last_name=last_name, middle_name=middle_name, phone_no=phone_no)
        new_acc.save()
        return redirect('index')


  return render(request, 'signup.html')


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('index')
    else:
      messages.info(request, "Invalid Input")
      return render(request, 'signin.html')

  return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
  auth.logout(request)
  return redirect('signin')


@login_required(login_url='signin')
def searchbar(request):
  user = User.objects.get(username=request.user.username)
  query = request.GET.get('search-area')
  all_search = SearchRec.objects.filter(acc=user)
  number = 0
  context = {
    'history':all_search
  }

  if query:
    result = []
    result_acc = []
    all_users = User.objects.all()

    for i in all_search:
      if query == i.query:
        number = number + 1
      else:
        pass
    
    if number == 0:
      new_search = SearchRec.objects.create(acc=user, query=query)
      new_search.save()
    else:
      pass

    for i in all_users:
      if query.lower() in i.first_name.lower() or query.lower() in i.username.lower() or query.lower() in i.last_name.lower():
        result.append(i)
    for i in result:
        acc_obj = Accounts.objects.get(user_main=i)
        result_acc.append(acc_obj)
      
    context = {
      'result':result_acc,
      'query':query,
      'history':all_search
    }

  

  return render(request, 'search.html', context)


#finance functionalities

@login_required(login_url='signin')
def deposit_screen(request):
  user = User.objects.get(username=request.user.username)
  acc = Accounts.objects.get(user_main=user)

  context = {
    'acc':acc
  }

  return render(request, 'deposit.html', context)


@login_required(login_url='signin')
def deposit_function(request):
  user = User.objects.get(username=request.user.username)
  acc_obj = Accounts.objects.get(user_main=user)
  
  if request.method == 'POST':
    pin = request.POST['pin']
    amount = request.POST['amount']
    amount = float(amount)

    if amount > 1000000.0:
      messages.info(request,'Too much')
      return redirect('depo-screen')
    else:
      if pin == acc_obj.transaction_pin:
        if amount != 0.00 or amount > 0.00:
          former = acc_obj.acc_balance
          acc_obj.acc_balance = acc_obj.acc_balance + amount
          acc_obj.save()
          new_dep = Deposit.objects.create(acc=acc_obj, amount=amount)
          new_dep.save()
          if acc_obj.acc_balance > former:
            messages.info(request,'Successful')
            return redirect('depo-screen')
          else:
            messages.info(request,'Declined')
            return redirect('depo-screen')
        else:
          messages.info(request,'Invalid Amount')
          return redirect('depo-screen')

      else:
        messages.info(request,'Pin Incorrect!')
        return redirect('depo-screen')




@login_required(login_url='signin')
def withdraw_screen(request):
  user = User.objects.get(username=request.user.username)
  acc = Accounts.objects.get(user_main=user)

  context = {
    'acc':acc
  }

  return render(request, 'withdraw.html', context)


@login_required(login_url='signin')
def withdraw_function(request):
  user = User.objects.get(username=request.user.username)
  acc_obj = Accounts.objects.get(user_main=user)
  
  if request.method == 'POST':
    pin = request.POST['pin']
    amount = request.POST['amount']
    amount = float(amount)

    if pin == acc_obj.transaction_pin:
      if amount != 0.00 or amount > 0.00:
        if amount < acc_obj.acc_balance:
          former = acc_obj.acc_balance
          acc_obj.acc_balance = acc_obj.acc_balance - amount
          acc_obj.save()
          new_dep = Withdraw.objects.create(acc=acc_obj, amount=amount)
          new_dep.save()
          if acc_obj.acc_balance < former:
            # transact = Withdraw.objects.filter(acc=acc_obj, amount=amount).last()
            # context = {
            #   'alert':'Successful',
            #   'amount':amount,
            #   'transaction': transact
            # }
            messages.info(request, "Successful")
            return redirect('withdraw-screen')
          else:
            # context = {
            #   'alert':'Declined',
            #   'amount':amount
            # }
            messages.info(request, "Declined")
            return redirect('withdraw-screen')
        else:
          messages.info(request,'Insufficient Funds')
          return redirect('withdraw-screen')
      else:
        messages.info(request,'Invalid Amount')
        return redirect('withdraw-screen')

    else:
      messages.info(request,'Pin Incorrect!')
      return redirect('withdraw-screen')


def send_screen(request):
  user = User.objects.get(username=request.user.username)
  acc = Accounts.objects.get(user_main=user)
  query = request.GET.get('search-area')
  receiver = ''
  # result_acc = []

  if query:
    receiver = Accounts.objects.get(acc_number=query)

  context = {
    'recipient':receiver
  }

  return render(request, 'send.html', context)


def send_func(request):
  user = User.objects.get(username=request.user.username)
  acc = Accounts.objects.get(user_main=user)

  if request.method == 'POST':
    pin = request.POST['pin']
    description = request.POST['description']
    receiver = request.POST['receiver_id']
    amount = request.POST['amount']
    amount = float(amount)

    recipient = Accounts.objects.get(acc_number=receiver)
    # recipient_user = User.objects.get()

    if pin == acc.transaction_pin:
      if amount < acc.acc_balance:
        acc.acc_balance = acc.acc_balance - amount
        recipient.acc_balance = recipient.acc_balance + amount
        acc.save()
        recipient.save()

        new_send = Send.objects.create(sender=user.username, description=description, amount=amount, receiver=recipient.user_main.username)
        new_send.save()

        #message-notification
        
        rooms = ChatRoom.objects.all()
        my_rooms = []
        main_room = []
        chatView ='n'
        # main_room = ''

        for i in rooms:
          if i.userA == request.user.username and i.userB == recipient.user_main.username:
            chatView = 'y'
            main_room.append(i)
          elif i.userA == recipient.user_main.username and i.userB == request.user.username:
            chatView = 'y'
            main_room.append(i)
        if chatView != 'y':
          room_make(request.user.username, recipient.user_main.username)
          rooms = ChatRoom.objects.all()
          for i in rooms:
            if i.userA == request.user.username and i.userB == recipient.user_main.username:
              chatView = 'y'
              main_room.append(i)


        if main_room:
          for i in main_room:
            notif_text = ChatMsg.objects.create(home=i, text_body=f"{user.username} sent {recipient.user_main.username} ${amount}", msg_type='notification', acc=user)
            notif_text.save()



        messages.info(request,'Successful')
        return redirect('send')
      else:
        messages.info(request,'Insufficient Fund')
        return redirect('send')
    else:
      messages.info(request,'Incorrect Pin')
      return redirect('send')


