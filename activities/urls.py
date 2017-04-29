from django.conf.urls import url

from activities import views

urlpatterns = [
    url(r'^orders/create$', views.create_order, name='create_order'),
    url(r'^orders/get_company_list$', views.get_company_list, name='get_company_list_order'),
]
