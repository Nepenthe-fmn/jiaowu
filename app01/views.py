from django.shortcuts import render,redirect,HttpResponse
from app01 import models
import json
# Create your views here.
# 首页
def index(req):
    username=req.session.get("username")
    print(username)
    if username:
        return render(req,"index.html",{"username":username})
    else:
        return redirect("/login/")
# 用户登录
def login(req):
    message=""
    if req.method == 'POST':
        userid = req.POST.get("userid")
        password = req.POST.get("password")
        # print(userid,password)
        userpwd=models.UserInfo.objects.filter(userid=userid,password=password).count()
        print(userpwd)
        if userpwd:
            username = models.UserInfo.objects.filter(userid=userid).values("username")
            username = username[0]["username"]
            print(username)
            req.session["is_login"]=True
            req.session["username"]=username
            req = redirect("/index/")
            return req
        else:
            message="用户名或密码错误"
    return render(req,"login.html",{"msg":message})
# 用户注册
def register(req):
    if req.method == 'POST':
        versions=req.POST.get("versions",None)
        userid=req.POST.get("userid",None)
        username=req.POST.get("username",None)
        password=req.POST.get("password",None)
        password_answer=req.POST.get("password_answer",None)
        models.UserInfo.objects.create(
            userid=userid,
            username=username,
            password=password,
            password_answer=password_answer,
        )
        print(versions,userid,username,password,password_answer)
    return render(req,"register.html")
#班级管理
from django.utils.safestring import mark_safe
def classes(req):
    # 获取班级列表信息
    if req.method == "GET":
        num_pages = req.GET.get("p",1)
        piece_one = 10
        pages_list =[]
        page_obj = PagesHelp(num_pages,pages_list,piece_one)
        pages_list = page_obj.pages()
        pages_list = "".join(pages_list)
        class_mesage = page_obj.message()
        return render(req, "classes.html", {"class_mesage": class_mesage,"pages":mark_safe(pages_list)})
    if req.method == "POST":
        pop_dict={"status":True,"error":None,"data":None,"success":None}
        del_dict={"status":True,"error":None,"data":None,"success":None}
        update_dict={"status":True,"error":None,"data":None,"success":None}
        pop_classid = req.POST.get("pop_classid",None)
        pop_clasname = req.POST.get("pop_classname",None)
        del_classname = req.POST.get("classname",None)
        del_id = req.POST.get("id",None)
        update_classname = req.POST.get("second_classname",None)
        update_id = req.POST.get("second_id",None)
        print(update_classname,update_id)
        # pop_del = req.POST.get("del",None)
        # print(pop_classid,pop_clasname,pop_del)
        if pop_classid and pop_clasname:
            models.classes.objects.create(classid=pop_classid,classname=pop_clasname)
            pop_dict["success"] = "添加成功"
        elif del_classname and del_id:
            models.classes.objects.filter(classid=del_id,classname=del_classname).delete()
            del_dict["success"] = "删除成功"
        elif update_classname and update_id:
            cbv=models.classes.objects.filter(classid=update_id).update(classname=update_classname)
            print("cbv:",cbv)
            update_dict["success"] = "更新成功"
        else:
            pop_dict["status"] = False
            pop_dict["error"] = "内容不能为空"
            del_dict["status"] = False
            del_dict["error"] = "删除失败"
            update_dict["status"] = False
            update_dict["error"] = "更新失败"
        if pop_dict["success"] == "添加成功":
            return HttpResponse(json.dumps(pop_dict))
        elif del_dict["success"] == "删除成功":
            return HttpResponse(json.dumps(del_dict))
        elif update_dict["success"] == "更新成功":
            return HttpResponse(json.dumps(update_dict))
#学生管理
def students(req):
    return render(req,"students.html")
#教师管理
def teachers(req):
    return render(req,"teachers.html")
#分页管理
class PagesHelp:
    # 构造函数
    def __init__(self,num_pages,pages_list,piece_one):
        self.num_pages=int(num_pages)
        self.pages_list=pages_list
        self.piece_one = piece_one
        self.pieces = models.classes.objects.count()
    #显示信息
    def message(self):
        start = (self.num_pages - 1) * self.piece_one
        end = self.num_pages * self.piece_one
        class_mesage = models.classes.objects.all()[start:end]
        # print(start, end, self.pieces)
        # print(class_mesage)
        return class_mesage
    # 分页
    def pages(self):
        num_pages = self.num_pages
        pages, pages_piece = divmod(self.pieces, self.piece_one)
        pages = pages + 1
        self.pages_list.append('<a href="/classes/?p=%s">[首页]</a>' % (1))
        if num_pages > 1:
            self.pages_list.append('<a href="/classes/?p=%s">[上一页]</a>' % (num_pages - 1))
        elif num_pages < 2:
            self.pages_list.append('<a href="/classes/?p=%s">[上一页]</a>' % (1))
        if pages > 5:
            if num_pages < 3:
                for i_pages in range(1, 6):
                    self.pages_list.append('<a href="/classes/?p=%s">[%s]</a>' % (i_pages, i_pages))
            elif 2 < num_pages < pages - 2:
                for i_pages in range(num_pages - 2, num_pages + 1 + 2):
                    self.pages_list.append('<a href="/classes/?p=%s">[%s]</a>' % (i_pages, i_pages))
            elif pages - 3 < num_pages < pages + 1:
                for i_pages in range(pages - 4, pages + 1):
                    self.pages_list.append('<a href="/classes/?p=%s">[%s]</a>' % (i_pages, i_pages))
        elif pages < 5:
            for i_pages in range(1, pages):
                self.pages_list.append('<a href="/classes/?p=%s">[%s]</a>' % (i_pages, i_pages))
        if num_pages < pages:
            self.pages_list.append('<a href="/classes/?p=%s">[下一页]</a>' % (num_pages + 1))
        elif num_pages > pages - 1:
            self.pages_list.append('<a href="/classes/?p=%s">[下一页]</a>' % (pages))
        self.pages_list.append('<a href="/classes/?p=%s">[尾页]</a>' % (pages))
        return self.pages_list
