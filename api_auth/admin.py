from django.contrib import admin

# Register your models here.
from .models import Wallet, Transaction

admin.site.register(Wallet)
admin.site.register(Transaction)