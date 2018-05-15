
import django_filters
from rest_framework import filters

from stu.models import Student


class StuFilter(filters.FilterSet):
    #  lookup_expr不写，精确搜索，写了，模糊搜索
    name = django_filters.CharFilter('s_name', lookup_expr='icontains') # 模糊搜索
    tel = django_filters.CharFilter('s_tel') # 精确搜索
    status = django_filters.CharFilter('s_status')
    operate_time_min = django_filters.DateTimeFilter('s_operate_time',lookup_expr='gte')
    operate_time_max = django_filters.DateTimeFilter('s_operate_time', lookup_expr='lte')
    yuwen_min = django_filters.NumberFilter('s_yuwen',lookup_expr='gte')
    yuwen_max = django_filters.NumberFilter('s_yuwen', lookup_expr='lte')

    class Meta:
        model = Student
        fields = ['s_name','s_tel','status','s_operate_time','s_yuwen']
