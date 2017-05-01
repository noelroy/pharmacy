from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from usershop.models import ShopStock


# Create your views here.


def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        search_location = request.GET.get('loc').strip()
        if len(querystring) == 0:
            return redirect('/search/')
        if len(search_location) == 0:
            return redirect('/search/')

        results = ShopStock.objects.filter(medicine__name__icontains=querystring).filter(
            Q(profile__address__line1__icontains=search_location) | Q(
                profile__address__line2__icontains=search_location) | Q(
                profile__address__city__icontains=search_location) | Q(
                profile__address__state__icontains=search_location) | Q(
                profile__address__country__icontains=search_location)).values('profile__address__email','profile__address__contactno','profile__address__pincode','profile__address__country','profile__address__state','profile__address__city','profile__address__line2','profile__address__line1','profile__name').distinct()

        return render(request, 'search/results.html', {
            'querystring': querystring,
            'search_location': search_location,
            'results': results,
        })
    else:
        return render(request, 'search/search.html')
