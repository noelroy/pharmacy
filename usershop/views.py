from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from authentication.models import Profile
from usershop.forms import StockForm
from django.contrib import messages
from usershop.models import ShopStock
from activities.models import Order, Transaction, Notification
from useradmin.models import Medicine
# Create your views here.

def shop_home(request):
    return render(request, 'usershop/home.html')

@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            new_stock = form.save(commit=False)
            new_stock.profile = request.user.profile
            new_stock.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Stock was successfully added.')
            form = StockForm()

    else:
        form = StockForm()
    return render(request, 'usershop/add_stock.html', {'form': form})


@login_required
def view_stocks(request):
    stocks = ShopStock.objects.filter(profile = request.user.profile)
    querystring = ''
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        stocks = stocks.filter(medicine__name__icontains=querystring)
    paginator = Paginator(stocks, 10)
    page = request.GET.get('page')
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        stocks = paginator.page(1)
    except EmptyPage:
        stocks = paginator.page(paginator.num_pages)
    return render(request, 'usershop/view_stocks.html', {'stocks': stocks, 'querystring': querystring})

@login_required
def view_avail_stocks(request):
    stocks = request.user.profile.get_avail_med()
    querystring = ''
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        stocks = stocks.filter(medicine__name__icontains=querystring)
    paginator = Paginator(stocks, 10)
    page = request.GET.get('page')
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        stocks = paginator.page(1)
    except EmptyPage:
        stocks = paginator.page(paginator.num_pages)
    return render(request, 'usershop/view_avail_stocks.html', {'stocks': stocks, 'querystring': querystring})


@login_required
def edit_stock(request, pk):
    stock = ShopStock.objects.get(pk=pk)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Stock was successfully updated.')

    else:
        form = StockForm(instance=stock)
    return render(request, 'usershop/edit_stock.html', {'form': form,'pk':pk})

@login_required
def delete_stock(request, pk):
    stock = ShopStock.objects.get(pk=pk)
    stock.delete()
    return redirect('view_stock_shop')

@login_required
def view_orders(request):
    orders = Order.objects.filter(from_user = request.user.profile).order_by('approval')
    querystring = ''
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        orders = orders.filter(to_user__name__icontains=querystring)
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    return render(request, 'usershop/view_orders.html', {'orders': orders, 'querystring': querystring})

@login_required
def delete_order(request, pk):
    stock = Order.objects.get(pk=pk)
    stock.delete()
    return redirect('view_order_shop')

@login_required
def view_transactions(request):
    trans = Transaction.objects.filter(to_user=request.user.profile).order_by('trans_date')
    querystring = ''
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        trans = trans.filter(from_user__name__icontains=querystring)
    paginator = Paginator(trans, 10)
    page = request.GET.get('page')
    try:
        trans = paginator.page(page)
    except PageNotAnInteger:
        trans = paginator.page(1)
    except EmptyPage:
        trans = paginator.page(paginator.num_pages)
    return render(request, 'usershop/view_trans.html', {'trans': trans, 'querystring': querystring})

@login_required
def view_note(request):
    med_det = request.user.profile.get_avail_med()
    for med in med_det:
        if(med['mcount']<10):
            Notification(notification_type=Notification.STOCK_LOW, from_user=request.user.profile,
                         to_user=request.user.profile, medicine = Medicine.objects.get(pk=med['medicine'])).save()
    trans = Notification.objects.filter(to_user=request.user.profile)
    querystring = ''
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        trans = trans.filter(from_user__name__icontains=querystring)
    paginator = Paginator(trans, 10)
    page = request.GET.get('page')
    try:
        trans = paginator.page(page)
    except PageNotAnInteger:
        trans = paginator.page(1)
    except EmptyPage:
        trans = paginator.page(paginator.num_pages)
    return render(request, 'usershop/view_note.html', {'trans': trans, 'querystring': querystring})