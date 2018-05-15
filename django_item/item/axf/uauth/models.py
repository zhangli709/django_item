from django.db import models

# Create your models here.


# class Users(models.Model):
#
#     u_name = models.CharField(max_length=20)
#     u_password = models.CharField(max_length=255)
#     u_email = models.CharField(max_length=30, null=True)
#     u_icon = models.ImageField(upload_to='upload', null=True)
#     s_delete = models.BooleanField(default=0)
#     ticket = models.CharField(max_length=256, null=True)
#
#     class Meta:
#         db_table = 'axf_my_users'

# 创建一个子表，用一对一方法，
from goods.models import UserModel


class UserModelInfo(models.Model):
    ticket = models.CharField(max_length=256)
    outtime = models.DateTimeField(null=True)
    t = models.OneToOneField(UserModel, on_delete=models.CASCADE)


    class Meta:
        db_table = 'axf_users_info'