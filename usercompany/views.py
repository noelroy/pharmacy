from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from usercompany.forms import StockForm
from django.contrib import messages
from usercompany.models import CompanyStock
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
    stocks = CompanyStock.objects.filter(profile = request.user.profile).order_by('mfd_date')
    paginator = Paginator(stocks, 10)
    page = request.GET.get('page')
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        stocks = paginator.page(1)
    except EmptyPage:
        stocks = paginator.page(paginator.num_pages)
    return render(request, 'usercompany/view_stocks.html', {'stocks': stocks})


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
    return render(request, 'usercompany/edit_stock.html', {'form': form,'pk':pk})

@login_required
def delete_stock(request, pk):
    stock = CompanyStock.objects.get(pk=pk)
    stock.delete()
    return redirect('view_stock_company')