from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

# Create your views here.
from stu.models import Student, StudentInfo
from stu.serializers import StudentSerializer
from uauth.models import Users

import logging
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from stu.filters import StuFilter

logger = logging.getLogger('stu')


def index(request):
    if request.method == 'GET':
        # 获取cookie.
        # ticket = request.COOKIES.get('ticket')
        # if not ticket:
        #     return HttpResponseRedirect('/uauth/login')
        # if Users.objects.filter(u_ticket=ticket).exists():
        #     stuinfos = StudentInfo.objects.all()
        #     return render(request, 'index.html', {'stuinfos': stuinfos})
        # else:
        #         return HttpResponseRedirect('/uauth/login/')
        #return render(request, 'index.html', {'stuinfos':stuinfos})
    #if request.method == 'POST':

        stuinfos = StudentInfo.objects.all()
        # 状态信息放到日志里去，想要什么，就放什么进去
        logger.info('url: %s method:%s获取学生信息成功' % (request.path, request.method))
        return render(request, 'index.html', {'stuinfos': stuinfos})

def addStu(request):
    if request.method == 'GET':
        return render(request, 'addStu.html')
    if request.method == 'POST':
        # 跳转到学习详情方法中
        name = request.POST.get('name')
        tel = request.POST.get('tel')

        stu = Student.objects.create(
            s_name=name,
            s_tel=tel,
        )

        return HttpResponseRedirect(
            reverse('s:addinfo', kwargs={'stu_id': stu.id})
        )

def addStuInfo(request, stu_id):

    if request.method == 'GET':
        return render(request, 'addStuInfo.html',{'stu_id': stu_id})

    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        addr = request.POST.get('addr')

        # 添加头像图片
        img = request.FILES.get('img')

        StudentInfo.objects.create(
            i_addr=addr, s_id=stu_id, i_image=img,
        )
        return HttpResponseRedirect('/stu/index/')

def stuPage(request):

    if request.method == 'GET':
        page_id = request.GET.get('page_id', 1)
        stus = Student.objects.all()
        paginator = Paginator(stus, 3)
        page = paginator.page(int(page_id))
        return render(request, 'index_page.html', {'stus': page})


class StudentEdit(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    # 查询所有信息
    queryset = Student.objects.all()
    # 序列化
    serializer_class = StudentSerializer
    # 过滤
    filter_class = StuFilter

    def get_queryset(self):
        """
        排序
        :return:
        """
        query = self.queryset
        return query.filter(s_delete=0).order_by('-id')
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.s_delete = 1
        instance.save()
        return Response({'msg':'删除成功', 'code':'200'})

def showStus(request):

    if request.method == 'GET':
        return render(request, 'show.html')

# 作业
def search(request):
    if request.method == 'GET':
        return render(request, 'search.html')
    if request.method == 'POST':
        if request.POST.get('name') == '1':
            stus = Student.objects.filter(s_yuwen__lt='60')
            return render(request, 'show5.html',{'stus': stus})
        if request.POST.get('name') == '2':
            stus = Student.objects.filter(s_yuwen__lte='90', s_yuwen__gte='80')
            return render(request, 'show5.html',{'stus': stus})
        if request.POST.get('name') == '3':
            stus = Student.objects.filter(s_status='NEXT_SCH')
            return render(request, 'show5.html',{'stus': stus})
        if request.POST.get('name') == '4':
            stus = Student.objects.filter(s_operate_time__lte='2018-5-1', s_operate_time__gte='2018-3-1')
            return render(request, 'show5.html',{'stus': stus})
        if request.POST.get('name') == '5':
            stus = Student.objects.filter(s_yuwen__lte='90', s_yuwen__gte='80',s_operate_time__lte='2018-5-1', s_operate_time__gte='2018-3-1')
            return render(request, 'show5.html',{'stus': stus})



