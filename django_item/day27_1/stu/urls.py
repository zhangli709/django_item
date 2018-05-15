from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from stu import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'student', views.StudentEdit)

urlpatterns = [
    url(r'^index/',login_required(views.index)),
    url(r'^stuPage/', login_required(views.stuPage)),
    url(r'^addStu/', login_required(views.addStu), name='addstu'),
    url(r'^addStuInfo/(?P<stu_id>\d+)/', login_required(views.addStuInfo), name='addinfo'),
    url(r'^showStu/', views.showStus),
    # 作业
    url(r'^search/', views.search),
]

urlpatterns += router.urls