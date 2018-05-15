import random
import time

from django.contrib import auth
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from uauth.models import Users



def regist(request):

    if request.method == 'GET':

        return render(request, 'day6_register.html')

    if request.method == 'POST':
        # 注册
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 对数据进行加密
        password = make_password(password)

        Users.objects.create(
            u_name=name,
            u_password=password
        )
        return HttpResponseRedirect('/uauth/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'day6_login.html')

    if request.method == 'POST':
        # 如果登录成功，绑定参数到cookie中，set_cookie.
        name = request.POST.get('name')
        password = request.POST.get('password')

        if Users.objects.filter(u_name=name).exists():
            user = Users.objects.get(u_name=name)
            if check_password(password, user.u_password):
                s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
                ticket = ''
                for i in range(15):
                    # 获取随机的字符串
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK' + ticket + str(now_time)
                #ticket = 'agdoajsdgsd'
                # 绑定令牌到cookie里。
                response = HttpResponseRedirect('/stu/index/')
                # max_age 最大存活时间，秒
                response.set_cookie('ticket', ticket, max_age=30000)
                # 存在服务段
                user.u_ticket = ticket
                user.save()
                return response
            else:
                #return HttpResponse('用户名或密码错误')
                return render(request, 'day6_login.html', {'password': '用户名或密码错误'})
        else:
            return render(request, 'day6_login.html', {'name': '用户不存在'})
            #return HttpResponse('用户不存在')

def logout(request):

    if request.method == 'GET':
        response = HttpResponseRedirect('/uauth/login/')
        response.delete_cookie('ticket')
        # return HttpResponseRedirect('/uauth/login')
        return response

def djlogin(request):
    if request.method == 'GET':
        return render(request, 'day6_login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # 到数据库里面验证用户名和密码是否正确,true返回user数据
        user = auth.authenticate(username=name, password=password)
        if user:
            # 验证成功，登录
            auth.login(request,user)
            return HttpResponseRedirect('/stu/index/')
        else:
            return render(request, 'day6_login.html')

def djregist(request):

    if request.method == 'GET':
        return render(request, 'day6_register.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # create_user 是django自带的Users表用的创建方法。
        User.objects.create_user(username=name,password=password)
        return HttpResponseRedirect('/uauth/dj_login/')

def djlogout(request):

    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect('/uauth/dj_login/')