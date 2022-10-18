from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.
class AdminUser(AbstractUser):
    gender_choices = (
        ('male', '男'),
        ('female', '女')
    )
    nick_name = models.CharField('昵称', max_length=50, default='')
    birthday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=gender_choices, default='1')
    address = models.CharField('地址', max_length=100, default='')
    phone = models.CharField('手机号', max_length=20, null=True, blank=True, default='')
    profile_picture = models.ImageField('用户头像', blank=True, default='images/avatars/logo.png',
                                        upload_to='images/avatars/{}/{}/{}/{}'.format(datetime.now().year,
                                                                                      datetime.now().month,
                                                                                      datetime.now().day,
                                                                                      datetime.now().hour))
    update_time = models.DateTimeField('更新时间', auto_now=True)
