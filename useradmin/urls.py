from django.conf.urls import url

from useradmin import views

urlpatterns = [
    url(r'^home/$', views.admin_home, name='admin_home'),
    url(r'^approve/$', views.approve, name='approve'),
    url(r'^medicine/add$', views.add_medicine, name='add_medicine'),
    url(r'^medicine/view$', views.view_medicines, name='view_medicines'),
    url(r'^shop/$', views.shop, name='admin_shop_list'),
    url(r'^company/$', views.company, name='admin_company_list'),
]
