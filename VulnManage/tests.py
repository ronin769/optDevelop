from django.test import TestCase
from VulnManage.models import *
import re

# Django的单元测试基于unittest库
class VulnManageTestCase(TestCase):

    # 测试函数执行前执行
    def setUp(self):
        print("======in setUp")

    # 需要测试的内容
    def test_add(self):

        CnvdManage.objects.all().delete()

        # 多线程存储到数据库
        executor = ThreadPoolExecutor(max_workers=200)
        # dirname = os.getcwd()
        dirname = '/src/optDevelop/VulnManage/cnvdfile/'
        fileList = os.listdir(dirname)
        # print(fileList)
        for filename in fileList:
            task1 = executor.submit(createCnvdToMysql, dirname, filename)
            print(task1.result())    # result方法可以获取task的执行结果

        # 删除cnvdNumber 为空 的字段
        CnvdManage.objects.filter(Q(cnvdNumber='')).delete()
        CnvdManage.objects.filter(Q(cnvdNumber=None)).delete()


        result = "success"
        print(result)
        print("CNVD 初始化完成！")


    # self.assertEqual(student.name, 'aaa')

    # 需要测试的内容
    def test_check_exit(self):
        # self.assertEqual(0,  FireWallFile.objects.count())
        print("======in test_check_exit")


    # 测试函数执行后执行
    def tearDown(self):
        # pass
        print("======in tearDown")
        # address = AddressName.objects.all()
        #
        # for line in address:
        #     print(line.addressName)
        #     print(line.addressIP)
        #     print(line.aaddressComment)
