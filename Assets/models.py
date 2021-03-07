from django.db import models
import mongoengine


# apt install mysql
# from tinymce.models import HTMLField
# pip3 install django-tinymce
# 先生成应用 python3 manage.py startapp Assets --fake
# 设置数据里 setting
# 创建空数据库 create schema  `MiscDatabase` DEFAULT CHARACTER SET utf8;
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

# 富文本编辑器需要安装 pip3 install django-tinymce


class V2ECSManage(models.Model):
    eipAddress = models.CharField(max_length=100, default="", null=True)
    domain = models.CharField(max_length=1000, default="", null=True)
    systemName = models.CharField(max_length=100, default="", null=True)
    businessPeople = models.CharField(max_length=100, default="", null=True)
    DevelopPeople = models.CharField(max_length=100, default="", null=True)
    accessURL = models.CharField(max_length=1000, default="", null=True)
    instanceId = models.CharField(max_length=100, default="", null=True)
    instanceName = models.CharField(max_length=100, default="", null=True)
    loadBalancerId = models.CharField(max_length=100, default="", null=True)
    loadBalancerName = models.CharField(max_length=100, default="", null=True)
    natIpAddress = models.CharField(max_length=100, default="", null=True)
    networkType = models.CharField(max_length=100, default="", null=True)
    physicalHostName = models.CharField(max_length=100, default="", null=True)
    privateIpAddress = models.CharField(max_length=100, default="", null=True)
    projectId = models.CharField(max_length=100, default="", null=True)
    projectName = models.CharField(max_length=200, default="", null=True)
    regionId = models.CharField(max_length=100, default="", null=True)
    securityGroupIdList = models.CharField(max_length=100, default="", null=True)
    slbIp = models.CharField(max_length=100, default="", null=True)
    slbStatus = models.CharField(max_length=100, default="", null=True)
    slbport = models.CharField(max_length=100, default="", null=True)
    vpcId = models.CharField(max_length=100, default="", null=True)
    description = models.CharField(max_length=1000, default="", null=True)
    createTime = models.DateTimeField(null=True)
    startTime = models.DateTimeField(null=True)
    isDelete = models.BooleanField(default=False)  # 是否可删除


class ShaoBingYunManage(models.Model):
    vulName = models.CharField(max_length=100, null=True)  # 风险名称
    vulLevel = models.CharField(max_length=100, null=True)  # 风险等级
    vulURL = models.CharField(max_length=500, null=True)  # 风险地址
    vulStatus = models.CharField(max_length=100, null=True)  # 检测状态
    vulAddress = models.CharField(max_length=100, null=True)  # 资产地址
    vulIP = models.CharField(max_length=100, null=True)  # ip地址
    vulDomain = models.CharField(max_length=1000, null=True)  # 关联域名
    vulService = models.CharField(max_length=1000, null=True)  # 服务信息
    vulCoutry = models.CharField(max_length=100, null=True)  # 地理位置
    vulIsRepair = models.CharField(max_length=100, null=True)  # 风险状态
    vulIsHandle = models.CharField(max_length=100, null=True)  # 处理状态
    vulGroup = models.CharField(max_length=100, null=True)  # 资产分组
    vulMark = models.CharField(max_length=100, null=True)  # 标签
    vulScore = models.CharField(max_length=100, null=True)  # 漏洞评分
    vulID = models.CharField(max_length=100, null=True)  # 评分编号
    vulDescribe = models.CharField(max_length=500, null=True)  # 风险描述
    vulType = models.CharField(max_length=100, null=True)  # 风险类型
    vulDamage = models.CharField(max_length=500, null=True)  # 风险危害
    vulDetails = models.TextField(max_length=2000, null=True)  # 风险细节
    vulSuggest = models.CharField(max_length=500, null=True)  # 修复建议
    vulRequest = models.TextField(max_length=1000, null=True)  # 请求
    vulResponse = models.TextField(max_length=20000, null=True)  # 响应
    vulFirstFindTime = models.DateTimeField(null=True)  # 首次发现时间
    vulUpdateTime = models.DateTimeField(null=True)  # 最后更新时间
    isDelete = models.BooleanField(default=False)  # 是否可删除


class DomainManage(models.Model):
    departmentName = models.CharField(max_length=100, null=True)    # 部门名称
    systemName = models.CharField(max_length=100, null=True)        # 系统名称
    domainName = models.CharField(max_length=200, null=True)        # 域名
    SLBIP = models.CharField(max_length=100, null=True)             # SLB地址
    ECSIP = models.CharField(max_length=500, null=True)             # ECS地址
    SLBPort = models.CharField(max_length=100, null=True)           # SLB端口
    systemType = models.CharField(max_length=100, null=True)        # 系统类型
    accessURL = models.CharField(max_length=1000, null=True)        # 访问URL
    developmentCompany = models.CharField(max_length=1000, null=True)  # 开发单位
    extranetAccess = models.CharField(max_length=100, null=True)    # 外网访问
    businessPeople = models.CharField(max_length=100, null=True)    # 业务联系人
    businessPhone = models.CharField(max_length=100, null=True)     # 业务联系方式
    projectPeopleName = models.CharField(max_length=100, null=True) # 项目经理
    projectPeoplePhone = models.CharField(max_length=100, null=True)# 项目经理联系人
    DevelopPeople = models.CharField(max_length=100, null=True)     # 开发联系人
    DevelopPhone = models.CharField(max_length=100, null=True)      # 开发联系方式
    systemStatus = models.CharField(max_length=100, null=True)      # 系统状态
    systemMiddleware = models.CharField(max_length=2000, null=True) # 中间件
    systemDescribe = models.CharField(max_length=2000, null=True)   # 描述
    systemCommon = models.CharField(max_length=2000, null=True)     # 备注
    CreateTime = models.DateTimeField(max_length=100, null=True)    # 创建时间
    updateTime = models.DateTimeField(max_length=100, null=True)    # 修改时间
    CreatePeople = models.CharField(max_length=100, null=True)      # 创建人
    updatePeople = models.CharField(max_length=100, null=True)      # 修改人
    systemUsername = models.CharField(max_length=100, null=True)    # 账号
    systemPassword = models.CharField(max_length=100, null=True)    # 密码
    isDelete = models.BooleanField(default=False)                   # 是否可删除


class ProduceFirewallManage(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    protocol = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    pl_grp_profile = models.CharField(max_length=100, null=True)
    mode = models.CharField(max_length=100, null=True)
    enable = models.CharField(max_length=100, null=True)
    bingo = models.CharField(max_length=100, null=True)
    cur_conn_num = models.CharField(max_length=100, null=True)
    syslog = models.CharField(max_length=100, null=True)
    log_sess_start = models.CharField(max_length=100, null=True)
    log_sess_end = models.CharField(max_length=100, null=True)
    refer_id = models.CharField(max_length=100, null=True)
    mv_opt = models.CharField(max_length=100, null=True)
    szone_list = models.CharField(max_length=1000, null=True)
    dzone_list = models.CharField(max_length=1000, null=True)
    saddr_list = models.CharField(max_length=1000, null=True)
    saddr_content = models.CharField(max_length=1000, null=True)
    saddr_desc = models.CharField(max_length=1000, null=True)
    daddr_list = models.CharField(max_length=1000, null=True)
    daddr_content = models.CharField(max_length=1000, null=True)
    daddr_desc = models.CharField(max_length=1000, null=True)
    sev_list = models.CharField(max_length=1000, null=True)
    sev_content = models.CharField(max_length=1000, null=True)
    sev_desc = models.CharField(max_length=1000, null=True)
    tr_list = models.CharField(max_length=1000, null=True)
    user_list = models.CharField(max_length=1000, null=True)
    app_list = models.CharField(max_length=1000, null=True)
    flowstat = models.CharField(max_length=100, null=True)
    is_end = models.CharField(max_length=100, null=True)
    page = models.CharField(max_length=100, null=True)
    recordsTotal = models.CharField(max_length=100, null=True)
    recordsFiltered = models.CharField(max_length=100, null=True)
    eurl = models.CharField(max_length=1000, null=True)
    durl = models.CharField(max_length=1000, null=True)
    isDelete = models.BooleanField(default=False)                   # 是否可删除

class WorkFirewallManage(models.Model):
    src_ip = models.CharField(max_length=1000, null=True)
    src_ip_content = models.CharField(max_length=1000, null=True)
    dst_ip = models.CharField(max_length=1000, null=True)
    dst_ip_content = models.CharField(max_length=1000, null=True)
    description = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    group = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    log = models.CharField(max_length=100, null=True)
    priority = models.CharField(max_length=100, null=True)
    conflict_num = models.CharField(max_length=100, null=True)
    num = models.CharField(max_length=100, null=True)
    active_time = models.CharField(max_length=100, null=True)
    dst_zone = models.CharField(max_length=100, null=True)
    invalid_id = models.CharField(max_length=100, null=True)
    src_zone = models.CharField(max_length=100, null=True)
    last_hittime = models.DateTimeField(auto_now_add=True, null=True)
    not_hit_day = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    highlight = models.CharField(max_length=100, null=True)
    invalid_name = models.CharField(max_length=100, null=True)
    action = models.CharField(max_length=100, null=True)
    src_port = models.CharField(max_length=100, null=True)
    service_app = models.CharField(max_length=100, null=True)
    is_sc_create = models.CharField(max_length=100, null=True)
    down_interface = models.CharField(max_length=100, null=True)
    hit = models.CharField(max_length=100, null=True)
    isDelete = models.BooleanField(default=False)                   # 是否可删除



