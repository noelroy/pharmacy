from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from usercompany.forms import StockForm
from django.contrib import messages
from usercompany.models import CompanyStock
from activities.models import Order, Transaction, Notification
from usershop.models import ShopStock
from datetime import date


# Create your views here.

@login_required
def company_home(request):
    return render(request, 'usercompany/home.html')


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
    return render(request, 'usercompany/add_stock.html', {'form': form})


@login_required
def view_stocks(request):
    stocks = CompanyStock.objects.filter(profile=request.user.profile).order_by('mfd_date')
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
    return render(request, 'usercompany/view_stocks.html', {'stocks': stocks, 'querystring': querystring})


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
    return render(request, 'usercompany/view_avail_stocks.html', {'stocks': stocks, 'querystring': querystring})


@login_required
def edit_stock(request, pk):
    stock = CompanyStock.objects.get(pk=pk)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Stock was successfully updated.')
    else:
        form = StockForm(instance=stock)
    return render(request, 'usercompany/edit_stock.html', {'form': form, 'pk': pk})


@login_required
def delete_stock(request, pk):
    stock = CompanyStock.objects.get(pk=pk)
    stock.delete()
    return redirect('view_stock_company')


@login_required
def view_orders(request):
    orders = Order.objects.filter(to_user=request.user.profile).order_by('approval')
    querystring = ''
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        orders = orders.filter(from_user__name__icontains=querystring)
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    for order in orders:
        order.avail = order.to_user.get_avail_med_single(order.medicine.pk)
    return render(request, 'usercompany/view_orders.html', {'orders': orders, 'querystring': querystring})


@login_required
def accept_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.approval = True
    order.save()
    med_price = order.from_user.get_avail_med_price(order.medicine.pk)
    quantity_no = order.quantity
    company_stocks = order.to_user.get_med_list(order.medicine.pk)
    for cstock in company_stocks:
        if (quantity_no == 0):
            break
        if (cstock.quantity == 0):
            continue
        elif (cstock.quantity >= quantity_no):
            cstock.quantity = cstock.quantity - quantity_no
            cstock.save()
            shop_stock = ShopStock(profile=order.from_user, medicine=order.medicine, sup_date=date.today(),
                                   exp_date=cstock.exp_date,
                                   price=med_price, quantity=quantity_no, sold=0)
            shop_stock.save()
            quantity_no = 0
        else:
            quantity_no = quantity_no - cstock.quantity
            qua_avail = cstock.quantity
            cstock.quantity = 0
            cstock.save()
            shop_stock = ShopStock(profile=order.from_user, medicine=order.medicine, sup_date=date.today(),
                                   exp_date=cstock.exp_date,
                                   price=med_price, quantity=qua_avail, sold=0)
            shop_stock.save()
    transaction = Transaction(from_user=order.to_user, to_user=order.from_user, quantity=order.quantity, order_id=order,
                              medicine=order.medicine,
                              total_price=(int(order.quantity) * order.to_user.get_avail_med_price(order.medicine.pk)))
    transaction.save()
    Notification(notification_type = Notification.ORDER_ACCEPTED,from_user = order.to_user,to_user = order.from_user, order = order).save()
    return redirect('view_order_company')


@login_required
def decline_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.approval = False
    order.save()
    Notification(notification_type = Notification.ORDER_DECLINED,from_user = order.to_user,to_user = order.from_user, order = order).save()
    return redirect('view_order_company')

@login_required
def view_transactions(request):
    trans = Transaction.objects.filter(from_user=request.user.profile).order_by('trans_date')
    querystring = ''
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        trans = trans.filter(to_user__name__icontains=querystring)
    paginator = Paginator(trans, 10)
    page = request.GET.get('page')
    try:
        trans = paginator.page(page)
    except PageNotAnInteger:
        trans = paginator.page(1)
    except EmptyPage:
        trans = paginator.page(paginator.num_pages)
    return render(request, 'usercompany/view_trans.html', {'trans': trans, 'querystring': querystring})