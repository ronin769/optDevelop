from django.test import TestCase
from Assets.models import *
import re

# Django的单元测试基于unittest库
class AssetsTestCase(TestCase):

    # 测试函数执行前执行
    def setUp(self):
        print("======in setUp")

    # 需要测试的内容
    def test_add(self):
        filepath = 'static/upload/pf.log'
        f = open(filepath, 'r')
        fileContent = f.readlines()
        for line in fileContent:

            line = line.strip()
            # print(line)
            if line.startswith("rule add"):















                ruleId = ''
                for id in re.findall('id (.*?) name', line):
                    ruleId = ruleId + " " + id

                ruleName = ""
                for name in re.findall('name "(.*?)" sa', line):
                    ruleName = ruleName + " " + name

                ruleSa = ""
                for sa in re.findall('sa (.*?) da', line):
                    ruleSa = ruleSa + " " + sa

                ruleDa = ""
                for da in re.findall('da "(.*?)" izone', line):
                    ruleDa = ruleDa + " " + da

                ruleIzone = ""
                for izone in re.findall('izone (.*?) ozone', line):
                    ruleIzone = ruleIzone + " " + izone

                ruleOzone = ""
                for ozone in re.findall('ozone (.*?) service', line):
                    ruleOzone = ruleOzone + " " + ozone

                ruleService = ""
                for service in re.findall('service (.*?) time', line):
                    ruleService = ruleService + " " + service

                ruleOpentime = ""
                for opentime in re.findall('time any log', line):
                    ruleOpentime = ruleOpentime + " " + opentime

                ruleStatus = ""
                for service in re.findall('service (.*?) time', line):
                    ruleStatus = ruleStatus + " " + service

                ruleActive = ""
                for active in re.findall('type (.*?) id', line):
                    ruleActive = ruleActive + " " + active


                comment = line.split(" ")[-1].replace('"', "")

                # ruleAccount = ""
                # for service in re.findall('service (.*?) time', line):
                #     ruleAccount = ruleAccount + " " + service








                print(ruleId, "-", ruleName, "-", ruleSa, "-", ruleDa, "-", ruleIzone, "-", ruleOzone, "-", ruleService, "-", ruleOpentime, "-", ruleStatus, "-", ruleActive, "-", comment)


                policy = PolicyManage()
                policy.ruleId = ruleId.encode('utf8')
                policy.ruleName = ruleName.encode('utf8')
                policy.ruleSa = ruleSa.encode('utf8')
                policy.ruleDa = ruleDa.encode('utf8')
                policy.ruleIzone = ruleIzone.encode('utf8')
                policy.ruleOzone = ruleOzone.encode('utf8')
                policy.ruleService = ruleService.encode('utf8')
                policy.ruleOpentime = ruleOpentime.encode('utf8')
                policy.ruleStatus = ruleStatus.encode('utf8')
                policy.ruleActive = ruleActive.encode('utf8')
                policy.ruleComment = comment.encode('utf8')
                policy.save()



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
