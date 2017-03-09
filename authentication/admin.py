from django.contrib import admin
from authentication.models import Profile
from authentication.models import Address
# Register your models here.

admin.site.register(Profile)
admin.site.register(Address)