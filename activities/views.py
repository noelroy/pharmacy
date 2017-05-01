from django.shortcuts import render
from useradmin.models import Medicine
from django.contrib.auth.decorators import login_required
from pharmacy.decorators import ajax_required
from django.http import JsonResponse
from usercompany.models import CompanyStock
from datetime import date
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from activities.models import Order
from authentication.models import Profile
from datetime import date

# Create your views here.
@login_required
def create_order(request):
    if request.method == "POST":
        medicinevalue = request.POST.get('medicineSelect', None)
        optionsRadios = request.POST.get('optionsRadios', None)
        quantity = request.POST.get('quantity',None)
        order = Order(from_user = request.user.profile, to_user = Profile.objects.get(pk=optionsRadios),medicine=Medicine.objects.get(pk=medicinevalue),quantity=quantity)
        order.save()
        messages.add_message(request,
                             messages.SUCCESS,
                             'Order was successfully placed.')
    medicines = Medicine.get_medicines()
    return render(request, 'activities/create_order.html', {'medicines': medicines})


@login_required
@ajax_required
def get_company_list(request):
    medicinevalue = request.GET.get('medicinevalue', None)
    company_list = CompanyStock.objects.filter(medicine__pk=medicinevalue).filter(exp_date__gt = date.today())
    html = ''
    html = '{0}{1}'.format(html,
                           render_to_string('activities/company_list.html',
                                            {
                                                'company_list': company_list,
                                            }))
    return HttpResponse(html)
