from django.db import models

# apt install mysql
# from tinymce.models import HTMLField
# pip3 install django-tinymce
# 先生成应用 python3 manage.py startapp FireWall
# 设置数据里 setting
# 创建空数据库 create schema  `optmanager` DEFAULT CHARACTER SET utf8;
# setting 中加入应用名'booktest'
# 定义以下类之后生成迁移 python3 manage.py makemigrations ，自动生成 00001_initial.py，为数据库
# 迁移 python3 manage.py migrate
# 当执行 python manage.py makemigrations 出现错误：TypeError: init() missing 1 required positional argument: ‘on_delete’
#   添加 book = models.ForeignKey('BookInfo', on_delete=models.CASCADE)
# 提示decode错误 query = query.decode(errors=‘replace’) 将decode修改为encode即可
# 定义url: index类
# from django.urls import path
# from . import views
# # 定义自己的 URL
# urlpatterns = [path('', views.index, name='index'),]
# 创建模板文件,index.html
# views 中修改返回值,会返回给index.html
# 运行 python3 manage.py runserver
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.utils.timezone as timezone
# 富文本编辑器需要安装 pip3 install django-tinymce


#设置菜单
class Menu(models.Model):
    menuTitle = models.CharField(u'菜单标题', max_length=25, unique=True)
    menuIcon = models.CharField(u'菜单图标', max_length=50)
    # menuLink = models.CharField(u'菜单链接', max_length=100)
    isDelete = models.BooleanField(default=False)   # 是否可删除

    parent = models.ForeignKey('self', verbose_name=u'父菜单', related_name='menu_menu', null=True, blank=True, on_delete=models.CASCADE)

    # def __str__(self):
    #     #显示层级菜单
    #     title_list = [self.title]
    #     p = self.parent
    #     while p:
    #         title_list.insert(0,p.title)
    #         p = p.parent
    #     return '-'.join(title_list)

#设置访问链接
class UserPermission(models.Model):
    PermissionName = models.CharField(u'权限标题', max_length=50, unique=True)
    PermissionIsMenu = models.BooleanField(u'菜单显示', default=False)
    PermissionUrl = models.CharField(max_length=128)
    PermissionMenu = models.ForeignKey(Menu, null=True, verbose_name=u'权限菜单', related_name='PermissionMenu',on_delete=models.CASCADE)

    # def __str__(self):
    #     return '{menu}--{permission}'.format(menu=self.menu, permission=self.title)

#设置角色和权限
class UserRole(models.Model):
    roleName = models.CharField(u'角色名称', max_length=25, unique=True)
    rolePermissionMenu = models.ManyToManyField(UserPermission, verbose_name=u'权限菜单', related_name='rolePermissionMenu')

    # def __str__(self):
    #     return self.title

REQUEST_STATUS=(
    ('0', '待审批'),
    ('1', '审批通过'),
    ('2', '审批拒绝'),
)

#注册有审批时使用
class UserRegister(models.Model):
    userEmail = models.EmailField('申请邮箱')
    userPhone = models.EmailField('申请手机')
    userName = models.CharField('用户名', max_length=50)
    userPasswd = models.CharField('用户密码', max_length=100, default="qwe123!@#")
    userStatus = models.CharField('审批状态', max_length=50, default='0', choices=REQUEST_STATUS)
    userIsCheck = models.BooleanField('是否审批', default=False)
    userIsUse = models.BooleanField('是否使用', default=False)
    userRole = models.ForeignKey(UserRole, verbose_name=u'账号权限', related_name='userRole', on_delete=models.CASCADE)
    userStarttime = models.DateTimeField('申请时间', auto_now_add=True)
    userUpdatetime = models.DateTimeField('审批时间', auto_now=True)
    userActionUser = models.ForeignKey(User, related_name='regist_for_actionuser', on_delete=models.CASCADE,null=True)
    # def __str__(self):
    #     return self.email


#重置密码时使用
class UserResetpasswd(models.Model):
    UserResetpasswdEmail = models.EmailField('申请邮箱')
    urlarg = models.CharField('重置参数', max_length=50)
    UserResetpasswdIsCheck = models.BooleanField('是否使用', default=False)
    UserResetpasswdUpdatetime = models.DateField('更新时间', auto_now=True)
    # def __str__(self):
    #     return self.email




#用户附加属性
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userPosition = models.CharField(u'职位名称', max_length=50)
    userPhone = models.CharField(u'手机号码', max_length=50)
    userDescription = models.TextField(u'用户简介')
    userLoginErrorCount = models.IntegerField(u'错误登陆', default=0)
    userLockTime = models.DateTimeField(u'锁定时间', default=timezone.now)
    userRole = models.ManyToManyField(UserRole, verbose_name=u'所属角色', related_name='user_role')

    # def __str__(self):
    #     return self.user.username


class MobilePasswd(models.Model):
    mobile = models.CharField(max_length=200, null=True)     # 文件路径
    passwd = models.CharField(max_length=200, null=True)     # 文件名字
    isDelete = models.BooleanField(default=False)   # 是否可删除



