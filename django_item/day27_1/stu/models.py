from django.db import models

# Create your models here.


class Student(models.Model):

    s_name = models.CharField(max_length=20)
    s_tel = models.CharField(max_length=11)
    s_yuwen = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    s_operate_time = models.DateTimeField(null=True)
    STATUS = [
        ('NONE', '正常'),
        ('NEXT_SCH', '留级'),
        ('DROP_SCH', '退学'),
        ('LEAVE_SCH', '休学')
    ]
    s_status = models.CharField(max_length=30,choices=STATUS,default='NONE')
    s_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'day27_1student'

class StudentInfo(models.Model):

    i_addr = models.CharField(max_length=30)
    i_image = models.ImageField(upload_to='upload',null=True)
    s = models.OneToOneField(Student)

    class Meta:
        db_table = 'day27_1student_info'

class Visit(models.Model):
    v_url = models.CharField(max_length=30)
    v_times = models.IntegerField()

    class Meta:
        db_table = 'day7_visit'