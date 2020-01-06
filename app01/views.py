from django.shortcuts import render,redirect,HttpResponse
from app01 import models
import json
# Create your views here.

# 注销用户
def logout(request):
    request.session.clear()
    return redirect("/login/")

# 用户登录
def login(req):
    message=""
    if req.method == 'POST':
        userid = req.POST.get("userid")
        password = req.POST.get("password")
        userpwd=models.UserInfo.objects.filter(userid=userid,password=password).count()
        if userpwd:
            username = models.UserInfo.objects.filter(userid=userid).values("username")
            username = username[0]["username"]
            req.session['is_login']=True
            req.session['username']=username
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
    return render(req,"register.html")

#权限管理（session）装饰器
def auth(func):
    def inner(request,*args,**kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request,*args,**kwargs)
        else:
            return redirect('/login/')
    return inner

# 首页
@auth
def index(req):
    username=req.session.get("username")
    if username:
        return render(req,"index.html",{"username":username})
    else:
        return redirect("/login/")

#班级管理
from django.utils.safestring import mark_safe
@auth
def classes(req):
    # 获取班级列表信息
    if req.method == "GET":
        num_pages = req.GET.get("p",1)
        piece_one = 10
        pages_list =[]
        page_name = 'classes'
        pieces=models.classes.objects.count()
        page_obj = PagesHelp(num_pages,pages_list,piece_one,pieces,page_name)
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
        if pop_classid and pop_clasname:
            models.classes.objects.create(classid=pop_classid,classname=pop_clasname)
            pop_dict["success"] = "添加成功"
        elif del_classname and del_id:
            models.classes.objects.filter(classid=del_id,classname=del_classname).delete()
            del_dict["success"] = "删除成功"
        elif update_classname and update_id:
            models.classes.objects.filter(classid=update_id).update(classname=update_classname)
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
@auth
def students(req):
    if req.method == "GET":
        num_pages = req.GET.get("p",1)
        piece_one = 10
        pages_list =[]
        page_name = 'classes'
        pieces=models.classes.objects.count()
        page_obj = PagesHelp(num_pages,pages_list,piece_one,pieces,page_name)
        pages_list = page_obj.pages()
        pages_list = "".join(pages_list)
        class_mesage = page_obj.message()
        return render(req, "students.html", {"class_mesage": class_mesage,"pages":mark_safe(pages_list)})
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
    # return render(req,"students.html")
#分页管理
class PagesHelp:
    # 构造函数
    def __init__(self,num_pages,pages_list,piece_one,pieces,page_name):
        self.num_pages=int(num_pages)
        self.pages_list=pages_list
        self.piece_one = piece_one
        self.pieces = pieces
        self.page_name=page_name
    #显示信息
    def message(self):
        start = (self.num_pages - 1) * self.piece_one
        end = self.num_pages * self.piece_one
        class_mesage = models.classes.objects.all()[start:end]
        return class_mesage
    def teacher_messgae(self):
        start = (self.num_pages - 1) * self.piece_one
        end = self.num_pages * self.piece_one
        teacher_list = models.teacher.objects.filter(id__in=models.teacher.objects.all()[start:end]).values('id',
        'teachername','cls__id','cls__classname')
        return teacher_list
    # 分页
    def pages(self):
        num_pages = self.num_pages
        pages, pages_piece = divmod(self.pieces, self.piece_one)
        pages = pages + 1
        self.pages_list.append('<a href="/%s/?p=%s">[首页]</a>' % (self.page_name,1))
        if num_pages > 1:
            self.pages_list.append('<a href="/%s/?p=%s">[上一页]</a>' % (self.page_name,num_pages - 1))
        elif num_pages < 2:
            self.pages_list.append('<a href="/%s/?p=%s">[上一页]</a>' % (self.page_name,1))
        if pages > 5:
            if num_pages < 3:
                for i_pages in range(1, 6):
                    self.pages_list.append('<a href="/%s/?p=%s">[%s]</a>' % (self.page_name,i_pages, i_pages))
            elif 2 < num_pages < pages - 2:
                for i_pages in range(num_pages - 2, num_pages + 1 + 2):
                    self.pages_list.append('<a href="/%s/?p=%s">[%s]</a>' % (self.page_name,i_pages, i_pages))
            elif pages - 3 < num_pages < pages + 1:
                for i_pages in range(pages - 4, pages + 1):
                    self.pages_list.append('<a href="/%s/?p=%s">[%s]</a>' % (self.page_name,i_pages, i_pages))
        elif pages < 5:
            for i_pages in range(1, pages+1):#1234
                self.pages_list.append('<a href="/%s/?p=%s">[%s]</a>' % (self.page_name,i_pages, i_pages))
        if num_pages < pages:
            self.pages_list.append('<a href="/%s/?p=%s">[下一页]</a>' % (self.page_name,num_pages + 1))
        elif num_pages > pages - 1:
            self.pages_list.append('<a href="/%s/?p=%s">[下一页]</a>' % (self.page_name,pages))
        self.pages_list.append('<a href="/%s/?p=%s">[尾页]</a>' % (self.page_name,pages))
        return self.pages_list

#教师管理
@auth
def teachers(req):
    if req.method == "GET":
        num_pages = req.GET.get("p",1)
        piece_one = 10
        pages_list =[]
        page_name = "teachers"
        pieces=models.teacher.objects.count()
        obj = PagesHelp(num_pages,pages_list,piece_one,pieces,page_name)
        pages_list = obj.pages()
        pages_list = "".join(pages_list)#列表转换成字符串
        teacher_list = obj.teacher_messgae()
        result = {}
        for obj in teacher_list:
            if obj['id'] in result:
                if obj['cls__id']:
                    result[obj['id']]['cls_list'].append({"id":obj["cls__id"],"classname":obj["cls__classname"]})
            else:
                if obj['cls__id']:
                    temp = [{'id':obj['cls__id'],'classname':obj['cls__classname']},]
                else:
                    temp = []
                result[obj['id']]={
                    'nid':obj['id'],
                    'name':obj['teachername'],
                    'cls_list':temp
                }
        # print(result)
        return render(req,"teachers.html",{"teacher_list":result,"pages":mark_safe(pages_list)})

#添加教师
@auth
def teacher_add(request):
    if request.method =="GET":
        cls_list = models.classes.objects.all()
        return render(request,"teacher_add.html",{"cls_list":cls_list})
    elif request.method =="POST":
        name = request.POST.get('teacher')
        cls = request.POST.getlist("cls")#存的是一个列表
        obj = models.teacher.objects.create(teachername=name)
        obj.cls.add(*cls)
        return render(request,"teacher_add.html")

#编辑教师
def edit_teacher(request,nid):
    if request.method == "GET":
        #已选择的教师的id
        obj = models.teacher.objects.get(id=nid)
        #获取当前老师已经管理的所有班级
        obj_list=obj.cls.all().values_list("classid","classname")#元组
        #已经管理的班级的ID列表
        id_list = list(zip(*obj_list))[0] if obj_list else [] #三元运算
        #获取不包括已经管理的班级
        cls_list=models.classes.objects.exclude(classid__in=id_list)
        return render(request,"edit_teacher.html",{"obj":obj,"cls_list":cls_list,"obj_list":obj_list})
    elif request.method == "POST":
        teachername = request.POST.get("name")
        cls_list = request.POST.getlist("cls")
        obj = models.teacher.objects.get(id=nid)
        obj.teachername = teachername
        obj.save()#单条数据添加
        obj.cls.set(cls_list)#课程添加
        return redirect("/teachers/")

#文件上传（Form表单）
@auth
def upload(request):
    if request.method == "GET":
        img_list = models.imagesurl.objects.all()
        return render(request,"upload.html",{"img_list":img_list})
    elif request.method == "POST":
        username = request.POST.get("username",None)
        #filesname = request.POST.get("files")
        file = request.FILES.get("files")
        import os
        path = os.path.join('statics', 'upload', file.name)
        f = open(path,'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        models.imagesurl.objects.create(filter=username,path=path)
        return redirect("/upload/")

#文件上传（FormData）
@auth
def uploadformdata(request):
    if request.method == "GET":
        img_list = models.imagesurl.objects.all()
        return render(request,"uploadformdata.html",{"img_list":img_list})
    elif request.method == "POST":
        username = request.POST.get("username",None)
        #filesname = request.POST.get("files")
        file = request.FILES.get("files")
        import os
        path = os.path.join('statics', 'upload', file.name)
        f = open(path,'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        models.imagesurl.objects.create(filter=username,path=path)
        ret = {'status':True,'path':path}
        return HttpResponse(json.dumps(ret))

#文件上传（iframe）
@auth
def uploadiframe(request):
    if request.method == "GET":
        img_list = models.imagesurl.objects.all()
        return render(request,"uploadiframe.html",{"img_list":img_list})
    elif request.method == "POST":
        username = request.POST.get("username",None)
        file = request.FILES.get("files")
        print(username,file)
        import os
        path = os.path.join('statics', 'upload', file.name)
        f = open(path,'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        models.imagesurl.objects.create(filter=username,path=path)
        ret = {'status':True,'path':path}
        return HttpResponse(json.dumps(ret))











