from django.conf.urls import url

from usercompany import views

urlpatterns = [
    url(r'^home/$', views.company_home, name='company_home'),
    url(r'^stock/add$', views.add_stock, name='add_stock_company'),
    url(r'^stock/view$', views.view_stocks, name='view_stock_company'),
    url(r'^stock/(?P<pk>\d+)/edit$', views.edit_stock, name='edit_stock_company'),
    url(r'^stock/(?P<pk>\d+)/delete$', views.delete_stock, name='delete_stock_company'),

]