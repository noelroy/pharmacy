from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from authentication.models import Profile
# Create your views here.

def shop_home(request):
    return render(request, 'usershop/home.html')