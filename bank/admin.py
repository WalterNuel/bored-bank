from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Accounts)
admin.site.register(Deposit)
admin.site.register(Send)
admin.site.register(Withdraw)
admin.site.register(SearchRec)
admin.site.register(SaveRecipient)