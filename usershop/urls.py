from django.conf.urls import url

from usershop import views

urlpatterns = [
    url(r'^home/$', views.shop_home, name='shop_home'),
    url(r'^stock/add$', views.add_stock, name='add_stock_shop'),
    url(r'^stock/view$', views.view_stocks, name='view_stock_shop'),
    url(r'^stock/avail_view$', views.view_avail_stocks, name='view_avail_stock_shop'),
    url(r'^stock/(?P<pk>\d+)/edit$', views.edit_stock, name='edit_stock_shop'),
    url(r'^stock/(?P<pk>\d+)/delete$', views.delete_stock, name='delete_stock_shop'),

    url(r'^order/view$', views.view_orders, name='view_order_shop'),
    url(r'^order/(?P<pk>\d+)/delete$', views.delete_order, name='delete_order_shop'),

    url(r'^transactions/view$', views.view_transactions, name='view_transactions_shop'),

    url(r'^note/view$', views.view_note, name='view_note_shop'),
]
