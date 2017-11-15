from django.conf.urls import url
from . import views

app_name = 'bidfeed'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
	
	#url(r'^(?P<product_id>[0-9]+)/$', views.profile, name='profile'),
    #url(r'^(?P<bid_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    #url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^create_product/$', views.create_product, name='create_product'),
	url(r'^user_bids/$', views.user_bids, name='user_bids'),
	url(r'^purchases/$', views.user_purchases, name='purchases'),
	url(r'^sale_products/$', views.sale_products, name='sale_products'),
    url(r'^(?P<product_id>[0-9]+)/place_bid/$', views.place_bid, name='place_bid'),
   
    url(r'^(?P<product_id>[0-9]+)/delete_product/$', views.delete_product, name='delete_product'),
]