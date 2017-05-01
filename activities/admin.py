from django.contrib import admin
from activities.models import Order, Transaction

# Register your models here.

admin.site.register(Order)
admin.site.register(Transaction)