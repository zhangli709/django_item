import random

from time import time

from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from goods.models import UserModel
from uauth.models import UserModelInfo
from utils.ticket import ticket_make


def regist(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        # 加密
        password = make_password(password)
        email = request.POST.get('email')
        img = request.FILES.get('icon')
        if UserModel.objects.filter(username=name).exists():
            return render(request, 'user/user_register.html', {'username': '用户名重复'})
        elif UserModel.objects.filter(email=email).exists():
            return render(request, 'user/user_register.html', {'email': '邮箱重复'})
        else:
            UserModel.objects.create(
                username=name,
                password=password,
                email=email,
                icon=img
            )
            return HttpResponseRedirect('/uauth/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        if UserModel.objects.filter(username=name).exists():
            password = request.POST.get('password')
            user = UserModel.objects.get(username=name)
            if check_password(password, user.password):
                # s = 'abcdefghijklmopqrstuvwxyz1234567890'
                # ticket = ''
                # for i in range(15):
                #     ticket += random.choice(s)
                # now_time = int(time())
                # ticket = 'TK' + ticket + str(now_time)

                # 获取ticket的方法单独写到函数中，直接调用
                ticket = ticket_make()

                response = HttpResponseRedirect('/goods/home/')
                # response.set_cookie('ticket', ticket, max_age=30000)expires过期的日期
                # 设置过期时间，首先拿到当前时间，再加上一天的时间，
                out_time = datetime.now() + timedelta(days=1)
                # 设置ticket，并且设置过期时间到页面。
                response.set_cookie('ticket', ticket, expires=out_time)
                # UserModelInfo.ticket = ticket
                # UserModelInfo.outtime = 3000
                # user.usermodelinfo.ticket = ticket

                if UserModelInfo.objects.filter(t_id=user.id).exists():
                    UserModelInfo.objects.update(ticket=ticket)
                    UserModelInfo.objects.update(outtime=out_time)
                else:

                    UserModelInfo.objects.create(
                        ticket=ticket,
                        outtime=out_time,
                        t_id=user.id
                    )
                return response
            else:
                return render(request, 'user/user_login.html')
        else:
            return render(request, 'user/user_login.html')


def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/goods/home/')
        response.delete_cookie('ticket')
        return response

