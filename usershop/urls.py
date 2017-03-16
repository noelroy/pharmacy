from django.conf.urls import url

from usershop import views

urlpatterns = [
    url(r'^home/$', views.shop_home, name='shop_home'),
    url(r'^stock/add$', views.add_stock, name='add_stock_shop'),
    url(r'^stock/view$', views.view_stocks, name='view_stock_shop'),
    url(r'^stock/(?P<pk>\d+)/edit$', views.edit_stock, name='edit_stock_shop'),
    url(r'^stock/(?P<pk>\d+)/delete$', views.delete_stock, name='delete_stock_shop'),
]
