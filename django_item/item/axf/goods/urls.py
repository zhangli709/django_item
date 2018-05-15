from django.conf.urls import url

from goods import views

urlpatterns = [
    # 主页，闪购，购物车，个人中心
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    # 闪购的详情展示，由于是三级分类，需要三个参数，所以每次都得传入三个参数，不够三个参数，得拿默认值来凑，否则报错
    url(r'^show/(\d+)/(\d+)/(\d+)/', views.show, name='show'),

    # 添加购物车
    url(r'^addgoods/', views.add_goods, name='addgoods'),
    url(r'^subgoods/', views.sub_goods, name='subgoods'),

    # 订单
    url(r'^order/', views.order),

    # 修改购物车商品选择
    url(r'^changeCartSelect/', views.user_change_select, name='change_select'),
    url(r'^cartsSelectAll/$', views.carts_select_all, name='select_all'),

    # 下单
    url(r'^generateOrder/', views.user_generate_order, name='user_generate_order'),
    # 支付页面
    url(r'^payOrder/(\d+)/', views.user_pay_order, name='user_pay_order'),

    # 订单详情
    url(r'^orderPayed/(\d+)/', views.order_pay, name='order_pay'),

    # 待付款
    url(r'^waitPayed/', views.wait_payed, name='wait_payed'),
    # 待收货
    url(r'^waitGet/', views.wait_get, name='wait_get'),
]