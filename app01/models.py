from django.db import models
# Create your models here.
class UserInfo(models.Model):
    userid=models.CharField(max_length=64)
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    password_answer=models.CharField(max_length=64)
class classes(models.Model):
    classid=models.CharField(max_length=64)
    classname=models.CharField(max_length=64)
class imagesurl(models.Model):
    filter = models.CharField(max_length=64)
    path = models.CharField(max_length=64)
class student(models.Model):
    studentname=models.CharField(max_length=64)
    email=models.CharField(max_length=64,null=True)
    cls = models.ForeignKey('Classes',on_delete=models.CASCADE)
class teacher(models.Model):
    teachername=models.CharField(max_length=64)
    cls = models.ManyToManyField('Classes')







