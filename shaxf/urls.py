from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home/$', views.home),


    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market),
    url(r'^cart/$', views.cart),
    #添加购物车
    url(r'^addCart/(\d+)/$', views.addCart),
    #
    url(r'^deal/$', views.deal),


    url(r'^mine/$', views.mine),
    url(r'^login/$', views.login),
    url(r'^quit/$', views.quit),
    url(r'^register/$', views.register),

    #订单详情页
    url(r'^detail/$', views.detail),

    # 订单商品详情页
    url(r'^allProducts/$', views.allProducts),

    # 总价
    url(r'allOk/$', views.allOk)


]