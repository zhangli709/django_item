from datetime import datetime
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from goods.models import UserModel
from uauth.models import UserModelInfo


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        中间键，用来判断是否登录，以及是否登录过期
        :param request:
        :return:
        """
        # if request.path == '/uauth/login/' or request.path == '/uauth/regist/':
        #     return None
        # ticket = request.COOKIES.get('ticket')
        # if not ticket:
        #     return HttpResponseRedirect('/uauth/login/')
        # users = UserModel.objects.filter(ticket=ticket)
        # if not users:
        #     return HttpResponseRedirect('/uauth/login/')
        # request.user = users[0]

        # ticket = request.COOKIES.get('ticket')
        # users = UserModelInfo.objects.filter(ticket=ticket)
        # if request.path == '/goods/cart/':
        #     if not ticket:
        #         return HttpResponseRedirect('/uauth/login/')
        #     if not users:
        #         return HttpResponseRedirect('/uauth/login/')
        # else:
        #     return None
        # request.user = users[0].t

        ticket = request.COOKIES.get('ticket')

        if not ticket:
            # 没有令牌，什么也不做
            return None
        # filter使用时，会变成列表，所有要对拿到的切片0，拿出里面的字典。
        users = UserModelInfo.objects.filter(ticket=ticket)
        if users:
            # 判读令牌是否有效，replace,转换时间，与下面对比比较。数据库里的时间，默认少8h,所有我们在当前时间减少8H，来和他比较
            out_time = users[0].outtime.replace(tzinfo=None)
            now_time = datetime.utcnow()

            if out_time > now_time:
                # 没有失效，通过正向查找，找到用户信息表
                request.user = users[0].t
            else:
                users.delete()


