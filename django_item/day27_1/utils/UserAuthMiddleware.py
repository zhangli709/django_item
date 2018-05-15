from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from uauth.models import Users


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 统一验证登录，
        # return none 或者不写

        if request.path == '/uauth/login/' or request.path == '/uauth/regist':
            return None
        ticket = request.COOKIES.get('ticket')
        # 如果ticket为空，
        if not ticket:
            return HttpResponseRedirect('/uauth/login/')

        # 如果ticket为空
        users = Users.objects.filter(u_ticket=ticket)
        if not users:
            return HttpResponseRedirect('/uauth/login/')

        request.user = users[0]