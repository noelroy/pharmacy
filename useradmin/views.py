from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from authentication.models import Profile
from pharmacy.decorators import ajax_required
from django.contrib.auth.models import User
from useradmin.forms import MedicineForm
from django.contrib import messages
from useradmin.models import Medicine
# Create your views here.

@login_required
def admin_home(request):
    unapproved_profiles = Profile.get_unapproved()
    paginator = Paginator(unapproved_profiles, 10)
    page = request.GET.get('page')
    try:
        unapproved_profiles = paginator.page(page)
    except PageNotAnInteger:
        unapproved_profiles = paginator.page(1)
    except EmptyPage:
        unapproved_profiles = paginator.page(paginator.num_pages)
    return render(request, 'useradmin/home.html', {'unapproved_profiles': unapproved_profiles})

@login_required
@ajax_required
def approve(request):
    username = request.POST['username']
    page_user = get_object_or_404(User, username=username)
    page_user.profile.approved = True
    page_user.save()
    return HttpResponse('<span class="glyphicon glyphicon-check"></span>Approved')

@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Medicine was successfully added.')
            form = MedicineForm()

    else:
        form = MedicineForm()
    return render(request, 'useradmin/add_medicine.html', {'form': form})

@login_required
def view_medicines(request):
    medicines = Medicine.get_medicines()
    paginator = Paginator(medicines, 10)
    page = request.GET.get('page')
    try:
        medicines = paginator.page(page)
    except PageNotAnInteger:
        medicines = paginator.page(1)
    except EmptyPage:
        medicines = paginator.page(paginator.num_pages)
    return render(request, 'useradmin/view_medicines.html', {'medicines': medicines})

@login_required
def shop(request):
    shops = Profile.get_shop()
    paginator = Paginator(shops, 10)
    page = request.GET.get('page')
    try:
        shops = paginator.page(page)
    except PageNotAnInteger:
        shops = paginator.page(1)
    except EmptyPage:
        shops = paginator.page(paginator.num_pages)
    return render(request, 'useradmin/shop_list.html', {'shops': shops})

@login_required
def company(request):
    companies = Profile.get_company()
    paginator = Paginator(companies, 10)
    page = request.GET.get('page')
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)
    return render(request, 'useradmin/company_list.html', {'companies': companies})