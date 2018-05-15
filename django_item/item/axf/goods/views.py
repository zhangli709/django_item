from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse

from goods.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, UserModel, Goods, CartModel, \
    OrderModel, OrderGoodsModel


def home(request):
    """
    主页渲染的实现
    :param request:
    :return: 返回首页渲染需要的数据库的数据
    """
    wheel = MainWheel.objects.all()
    nav = MainNav.objects.all()
    mustBuy = MainMustBuy.objects.all()
    shop = MainShop.objects.all()
    # shop1 = MainShop.objects.first()
    # shop2_3 = MainShop.objects.filter(id__lte=3, id__gte=2)
    # shop4_7 = MainShop.objects.filter(id__lte=7, id__gte=4)
    # shop8_11 = MainShop.objects.filter(id__lte=11, id__gte=8)
    show = MainShow.objects.all()
    data = {
        'wheels': wheel,
        'navs': nav,
        'mustBuys': mustBuy,
        'shops': shop,
        # 'shop1': shop[0],
        # 'shop2_3': shop[1:3],
        # 'shop4_7': shop[3:7],
        # 'shop8_11': shop[7:],
        'shows': show
    }

    return render(request, 'home/home.html', data)


def market(request):
    """
    传入闪购页面的默认参数，即分类一开始展示的页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        # foodtypes = FoodType.objects.all()
        # goods = Goods.objects.filter(categoryid=104749)
        # data = {
        #     'goods': goods,
        #     'foodtypes': foodtypes
        # }
        # return render(request, 'market/market.html', data)
        # 最开始展示一个以这个参数返回页面
        return HttpResponseRedirect(
            reverse('axf:show', args=('104749', '0', '0'))
        )


def show(request, typeid, cid, sort_id):
    """
    闪购页面，接收三级分类的参数，并渲染到页面
    :param request:
    :param typeid:
    :param cid:
    :param sort_id:
    :return:
    """
    # 获取分类类型，展示此表得每一条项目，一级分类
    foodtypes = FoodType.objects.all()
    # 全部分类来分类，在一级分类得基础上，再次分类
    if cid == '0':
        goods = Goods.objects.filter(categoryid=typeid)
    else:
        goods = Goods.objects.filter(categoryid=typeid, childcid=cid)

    # 排序，三级分类
    if sort_id == '0':
        goods = goods
    elif sort_id == '1':
        goods = goods.order_by('productnum')
    elif sort_id == '2':
        goods = goods.order_by('price')
    elif sort_id == '3':
        goods = goods.order_by('-price')
    # 全部分类名称，拿到二级分类得参数，重数据库里拿到分类方法。展示分类名称和分类方法
    listname = FoodType.objects.filter(typeid=typeid).first().childtypenames.split('#')
    names = []
    for i in listname:
        names.append(i.split(':'))
    data = {
        'goods': goods,
        'foodtypes': foodtypes,
        'names': names,  # 分类名称和分类id都在里面
        'typeid': typeid,
        'cid': cid,
        'sort_id': sort_id,
    }

    return render(request, 'market/market.html', data)


def mine(request):
    """
    对应展示mine这个页面的，关联表为UserModel，ordermodel这两个表。通过用户表，找到订单表，拿到信息，返回。
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 如果ticket有效，那么可请求到有值的user，否则user为空。
        user = request.user
        data = {}
        if user.id:
            # 主键表查外键表，拿到订单表里的数量
            orders = user.ordermodel_set.all()
            wait_pay, payed = 0, 0
            for order in orders:
                """遍历，每有一件，加一，这里的0和1代表有商品，参看建表时的说明。"""
                if order.o_status == 0:
                    wait_pay += 1
                elif order.o_status == 1:
                    payed += 1
            data = {
                'wait_pay': wait_pay,
                'payed': payed
            }

        return render(request, 'mine/mine.html', data)


def cart(request):
    if request.method == 'GET':
        # cartmodel = CartModel.objects.all()
        # goods = Goods.objects.all()
        # data = {
        #     'cartmodel': cartmodel,
        #     'goods': goods,
        # }
        user = request.user
        if user and user.id:
            carts = CartModel.objects.all()
            return render(request, 'cart/cart.html', {'carts': carts})
        else:
            return HttpResponseRedirect(reverse('u:login'))


def add_goods(request):
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        # 拿到用户，通过中间键拿到
        user = request.user
        if user and user.id:
            # 如果不为空，即有用户时，拿到ajax返回的值，
            goods_id = request.POST.get('goods_id')
            # 获取购物车信息
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if user_carts:
                # 如果存在这个商品，就修改数据，并且传入到
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                # 新建
                CartModel.objects.create(
                    user=user,
                    goods_id=goods_id,
                    c_num=1
                )
                data['c_num'] = 1
            # 返回json数据到ajax里，用来渲染。
        return JsonResponse(data)



def sub_goods(request):
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user
        goods_id = request.POST.get('goods_id')

        if user and user.id:
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()

            if user_carts:
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num

        return JsonResponse(data)


def user_change_select(request):
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user
        id = request.POST.get('id')
        if user and user.id:
            cart = CartModel.objects.filter(id=id).first()
            if cart.is_select:
                cart.is_select = False
            else:
                cart.is_select = True
            cart.save()
            data['is_select'] = cart.is_select
            carts_select = CartModel.objects.filter(is_select=True)
            count_price = 0
            for cart in carts_select:
                count_price += Goods.objects.get(id=cart.goods_id).price
            data['count_price'] = count_price
            return JsonResponse(data)


def carts_select_all(request):
    if request.method == 'GET':
        data = {
            'code': 200,
            'msg': '请求成功！'
        }
        carts = CartModel.objects.all()
        for cart in carts:
            cart.is_select = True
            cart.save()
        # data['carts'] = carts
        return JsonResponse(data)


def order(request):
    if request.method == 'GET':
        return render(request, 'order/order_info.html')


def user_generate_order(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            cart_goods = CartModel.objects.filter(is_select=True)
            # o_status =0 未付款，1为已付款,订单表
            order = OrderModel.objects.create(user=user, o_status=0)
            # 订单详情表
            for cart_good in cart_goods:
                OrderGoodsModel.objects.create(
                    order=order,  # 关联订单表
                    goods=cart_good.goods,  # 关联商品表
                    goods_num=cart_good.c_num  # 关联每个商品的数量
                )
                cart_good.delete()

            return HttpResponseRedirect(reverse('axf:user_pay_order', args=(order.id,)))


def user_pay_order(request, order_id):
    if request.method == 'GET':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        # 拿到订单表的信息
        orders = OrderModel.objects.filter(id=order_id).first()
        data['orders'] = orders
        data['order_id'] = order_id
        # order_goods = orders.ordergoodsmodel_set.all()
        # for order_good in order_goods:
        #     goods = Goods.objects.filter(id=order_goods.goods_id)
        return render(request, 'order/order_info.html', data)


def order_pay(request, order_id):
    # 修改订单的状态 o_status = 1
    if request.method == 'GET':
        OrderModel.objects.filter(id=order_id).update(o_status=1)
        return HttpResponseRedirect(reverse('axf:mine'))


def wait_payed(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            # 0 表示待支付，1表示待收货
            goods = OrderModel.objects.filter(o_status=0)
            return render(request, 'order/order_list_wait_pay.html', {'goods': goods})


def wait_get(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            # 找出数据库里待收货的商品，返回给页面
            goods = OrderModel.objects.filter(o_status=1)
            return render(request, 'order/order_list_payed.html', {'goods': goods})
