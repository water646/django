from django.db import models

# Create your models here.
#步骤：建立模型，迁移,修改DATABASE的参数连接数据库，在__init__导入数据库设置

class Chat(models.Model):
    text=models.TextField()
    outer=models.CharField(max_length=100,null=True)
    time=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['time']


class User(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)