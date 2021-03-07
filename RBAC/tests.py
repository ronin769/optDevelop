from django.test import TestCase
import re
import xlrd

# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optDevelop.settings')
# django.setup()

# from RBAC.models import *

# Django的单元测试基于unittest库
class RBACTestCase(TestCase):

    # 测试函数执行前执行
    def setUp(self):
        print("======in setUp")

    # 需要测试的内容
    def test_add(self):
        print("sssssssssssssss")
        # pass


    # 需要测试的内容
    def test_check_exit(self):
        # self.assertEqual(0,  FireWallFile.objects.count())
        print("======in test_check_exit")


    # 测试函数执行后执行
    def tearDown(self):
        # pass
        print("======in tearDown")

        # for line in address:
        #     print(line.addressName)
        #     print(line.addressIP)
        #     print(line.aaddressComment)
