from django.conf.urls import url

from usercompany import views

urlpatterns = [
    url(r'^home/$', views.company_home, name='company_home'),
    url(r'^stock/add$', views.add_stock, name='add_stock_company'),
]
