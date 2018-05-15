from django.db import models

# Create your models here.


# 父表，给下面四个表继承用
class Main(models.Model):
    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称
    trackid = models.CharField(max_length=16)  #通用id

    class Meta:
        abstract = True


class MainWheel(Main):
    # 轮播banner
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    # 必购
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


# 主页表
class MainShow(Main):
    categoryid = models.CharField(max_length=16)  # 虽然没有给出外键，但是这里的值和goods表里的categoryid一样，以此来查询goods表的数据
    brandname = models.CharField(max_length=100)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=1)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


# 闪购--左侧类型表
class FoodType(models.Model):
    typeid = models.CharField(max_length=16)  # 等于goods表的categoryid，和这个相互对应
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)  # 等于goods表里的childcid相互对应
    typesort = models.IntegerField(default=1)  # 对应于最后一级分类

    class Meta:
        db_table = 'axf_foodtypes'


# 商品表
class Goods(models.Model):
    productid = models.CharField(max_length=16)  # 商品id
    productimg = models.CharField(max_length=200)  # 商品的图片
    productname = models.CharField(max_length=100)  # 商品的名称
    productlongname = models.CharField(max_length=200)  # 商品的规格
    isxf = models.IntegerField(default=1)  #
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)  # 规格
    price = models.FloatField(default=0)  # 折后价格
    marketprice = models.FloatField(default=1)  # 原价
    categoryid = models.CharField(max_length=16)  # 分类id  #  对应一级分类的查找
    childcid = models.CharField(max_length=16)  # 子分类id  # 对应二级分类
    childcidname = models.CharField(max_length=100)  # 名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 排序
    productnum = models.IntegerField(default=1)  # 销量排序

    class Meta:
        db_table = 'axf_goods'


# 用户表
class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)  # 名称
    password = models.CharField(max_length=256)  # 密码
    email = models.CharField(max_length=64, unique=True)  # 邮箱
    # Flase 代表女
    sex = models.BooleanField(default=False)  # 性别
    icon = models.ImageField(upload_to='icon')  # 头像，需要上传头像，就需要创建media这个文件夹，并在settings写入查找连接
    is_delete = models.BooleanField(default=False)  # 是否删除

    class Meta:
        db_table = 'axf_users'


# 购物车
class CartModel(models.Model):
    user = models.ForeignKey(UserModel)  # 关联用户
    goods = models.ForeignKey(Goods)  # 关联商品
    c_num = models.IntegerField(default=1)  # 商品的个数
    is_select = models.BooleanField(default=True)  # 是否选择商品，默认选中

    class Meta:
        db_table = 'axf_cart'


# 订单表
class OrderModel(models.Model):
    user = models.ForeignKey(UserModel)  # 关联用户
    o_num = models.CharField(max_length=64)  # 数量，这里没有用到此条数据
    # 0表示已经下单，但是未付款，1表示已付款，未发货， 2已付款
    o_status = models.IntegerField(default=0)  # 状态
    o_create = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 'axf_order'


# 订单详情表
class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods)  # 关联商品表
    order = models.ForeignKey(OrderModel)  # 关联订单表，
    goods_num = models.IntegerField(default=1)  # 商品的个数

    class Meta:
        db_table = 'axf_order_goods'


