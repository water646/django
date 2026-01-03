

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.
#步骤：建立模型，迁移,修改DATABASE的参数连接数据库，在__init__导入数据库设置

class Chat(models.Model):
    text=models.TextField()
    outer=models.CharField(max_length=100,null=True)
    time=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['time']

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("用户名不能为空")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        # 🔥 authenticate() 就靠这个
        return self.get(username=username)


class User(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(max_length=100,unique=True)
    # password=models.CharField(max_length=100)
    reg_time=models.DateTimeField(default=timezone.now)
    root=models.BooleanField(default=False)
    headimg=models.CharField(max_length=100,default='')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # token=models.CharField(max_length=400,default='')

class Audio(models.Model):
    uploader=models.CharField(max_length=100)
    name=models.CharField(max_length=400)
    # duration=models.IntegerField()
    uploaded_time=models.DateTimeField(default=timezone.now)

# class User(AbstractUser):
#     reg_time=models.DateTimeField(default=timezone.now)
#     root=models.BooleanField(default=False)