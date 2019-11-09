from django.db import models
models.CharField()
# Create your models here.
class UserInfo(models.Model):
    userid=models.CharField(max_length=64)
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    password_answer=models.CharField(max_length=64)
class classes(models.Model):
    classid=models.CharField(max_length=64)
    classname=models.CharField(max_length=64)