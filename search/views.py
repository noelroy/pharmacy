from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from authentication.models import Profile

# Create your views here.


def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')

        results = Profile.objects.filter(
            Q(name__icontains=querystring))

        return render(request, 'search/results.html', {
            'querystring': querystring,
            'results': results,
        })
    else:
        return render(request, 'search/search.html')
