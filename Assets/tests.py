from django.test import TestCase
from Assets.models import *
import re
import xlrd


# Django的单元测试基于unittest库
class AssetsTestCase(TestCase):

    # 测试函数执行前执行
    def setUp(self):
        print("======in setUp")

    # 需要测试的内容
    def test_add(self):
        print("41523456456")
        pass
        # # 设置路径
        # path = 'static/upload/shaoBingYunThreat.xls'
        #
        # # 打开execl
        # workbook = xlrd.open_workbook(path)
        #
        # # 输出Excel文件中所有sheet的名字
        # print(workbook.sheet_names())
        #
        # # 根据sheet索引或者名称获取sheet内容
        # vulnSheet = workbook.sheets()[0]  # 通过索引获取
        # # ecsSheet = workbook.sheet_by_index(0)  # 通过索引获取
        # # ecsSheet = workbook.sheet_by_name('ECS')  # 通过名称获取
        #
        #
        # print(vulnSheet.name)  # 获取sheet名称
        # rowNum = vulnSheet.nrows  # sheet行数
        # colNum = vulnSheet.ncols  # sheet列数

        # # 获取所有单元格的内容
        # list = []
        # for i in range(rowNum):
        #     rowlist = []
        #     for j in range(colNum):
        #         rowlist.append(Data_sheet.cell_value(i, j))
        #
        #         print(type(date_value), date_value)
        #     list.append(rowlist)
        # print(list)

        #
        # # 输出所有单元格的内容
        # for row in range(rowNum):
        #     print(vulnSheet.cell_value(row, 0))
        #     print(vulnSheet.cell_value(row, 1))
        #     print(vulnSheet.cell_value(row, 2))
        #     print(vulnSheet.cell_value(row, 3))
        #     print(vulnSheet.cell_value(row, 4))
        #     print(vulnSheet.cell_value(row, 5))
        #     print(vulnSheet.cell_value(row, 6))
        #     print(vulnSheet.cell_value(row, 7))
        #     print(vulnSheet.cell_value(row, 8))
        #     print(vulnSheet.cell_value(row, 9))
        #     print(vulnSheet.cell_value(row, 10))
        #     print(vulnSheet.cell_value(row, 11))
        #     print(vulnSheet.cell_value(row, 12))
        #     print(vulnSheet.cell_value(row, 13))
        #     print(vulnSheet.cell_value(row, 14))
        #     print(vulnSheet.cell_value(row, 15))
        #     print(vulnSheet.cell_value(row, 16))
        #     print(vulnSheet.cell_value(row, 17))
        #     print(vulnSheet.cell_value(row, 18))
        #     print(vulnSheet.cell_value(row, 19))
        #     print(vulnSheet.cell_value(row, 20))
        #     print(vulnSheet.cell_value(row, 21))
        #     print(vulnSheet.cell_value(row, 22))
        #     print(vulnSheet.cell_value(row, 23))
        #     print(vulnSheet.cell_value(row, 24))
        #     print(vulnSheet.cell_value(row, 25))
        #     print(vulnSheet.cell_value(row, 26))
        #     print(vulnSheet.cell_value(row, 27))
        #     print(vulnSheet.cell_value(row, 28))
        #     print(vulnSheet.cell_value(row, 29))




            # for j in range(colNum):
            #     # # 获取单元格内容为日期的数据
            #     # date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(i, j), workbook.datemode)
            #     # print(date_value)
            #     print(ecsSheet.cell_value(row, j))
            #     # print(list[i][j], '\t\t', end="")
            #
            # ecsID = ecsSheet.cell_value(row, 0)
            # ecsName = ecsSheet.cell_value(row, 1)
            # ecsPartment = ecsSheet.cell_value(row, 2)
            # ecsProject = ecsSheet.cell_value(row, 3)
            # ecsZone = ecsSheet.cell_value(row, 4)
            # ecsStatus = ecsSheet.cell_value(row, 5)
            # ecsNetwork = ecsSheet.cell_value(row, 6)
            # ecsIP = ecsSheet.cell_value(row, 7)
            # ecsSLBIP = ecsSheet.cell_value(row, 8)
            # ecsCPU = ecsSheet.cell_value(row, 9)
            # ecsMemory = ecsSheet.cell_value(row, 10)
            # ecsSystemStore = ecsSheet.cell_value(row, 11)
            # ecsDataStore = ecsSheet.cell_value(row, 12)
            # ecsSystemOS = ecsSheet.cell_value(row, 13)
            # ecsDescribe = ecsSheet.cell_value(row, 14)
            # ecsComment = ecsSheet.cell_value(row, 15)
            #
            #
            # ecsobj = ECSManage()
            # ecsobj.ecsID = ecsID.encode('utf8')
            # ecsobj.ecsName = ecsName.encode('utf8')
            # ecsobj.ecsPartment = ecsPartment.encode('utf8')
            # ecsobj.ecsProject = ecsProject.encode('utf8')
            # ecsobj.ecsZone = ecsZone.encode('utf8')
            # ecsobj.ecsStatus = ecsStatus.encode('utf8')
            # ecsobj.ecsNetwork  = ecsNetwork .encode('utf8')
            # ecsobj.ecsIP = ecsIP.encode('utf8')
            # ecsobj.ecsSLBIP = ecsSLBIP.encode('utf8')
            # ecsobj.ecsCPU = str(ecsCPU).encode('utf8')
            # ecsobj.ecsMemory = str(ecsMemory).encode('utf8')
            # ecsobj.ecsSystemStore = str(ecsSystemStore).encode('utf8')
            # ecsobj.ecsDataStore = str(ecsDataStore).encode('utf8')
            # ecsobj.ecsSystemOS = ecsSystemOS.encode('utf8')
            # ecsobj.ecsDescribe = ecsDescribe.encode('utf8')
            # ecsobj.ecsComment = str(ecsComment).encode('utf8')
            # ecsobj.save()

        #
        # # 获取整行和整列的值（列表）
        # rows = Data_sheet.row_values(0)  # 获取第一行内容
        # cols = Data_sheet.col_values(1)  # 获取第二列内容
        # # print (rows)
        # # print (cols)
        #
        # # 获取单元格内容
        # cell_A1 = Data_sheet.cell(0, 0).value
        # cell_B1 = Data_sheet.row(0)[1].value  # 使用行索引
        # cell_C1 = Data_sheet.cell(0, 2).value
        # cell_D2 = Data_sheet.col(3)[1].value  # 使用列索引
        # print(cell_A1, cell_B1, cell_C1, cell_D2)
        #
        # # 获取单元格内容的数据类型
        # # ctype:0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        # print('cell(0,0)数据类型:', Data_sheet.cell(0, 0).ctype)
        # print('cell(1,0)数据类型:', Data_sheet.cell(1, 0).ctype)
        # print('cell(1,1)数据类型:', Data_sheet.cell(1, 1).ctype)
        # print('cell(1,2)数据类型:', Data_sheet.cell(1, 2).ctype)
        #
        # # 获取单元格内容为日期的数据
        # date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(1,0),workbook.datemode)
        # print(type(date_value), date_value)
        # print('%d:%d:%d' % (date_value[0:3]))
        #







    # self.assertEqual(student.name, 'aaa')

    # 需要测试的内容
    def test_check_exit(self):
        # self.assertEqual(0,  FireWallFile.objects.count())
        print("======in test_check_exit")


    # 测试函数执行后执行
    def tearDown(self):
        # pass
        print("======in tearDown")
        # ecsobjs = ECSManage.objects.filter()
        # for ecsobj in ecsobjs:
        #     print(ecsobj.ecsID)
        #     print(ecsobj.ecsName)
        #     print(ecsobj.ecsPartment)
        #     print(ecsobj.ecsProject)
        #     print(ecsobj.ecsZone)
        #     print(ecsobj.ecsStatus)
        #     print(ecsobj.ecsNetwork )
        #     print(ecsobj.ecsIP)
        #     print(ecsobj.ecsSLBIP)
        #     print(ecsobj.ecsCPU)
        #     print(ecsobj.ecsMemory)
        #     print(ecsobj.ecsSystemStore)
        #     print(ecsobj.ecsDataStore)
        #     print(ecsobj.ecsSystemOS)
        #     print(ecsobj.ecsDescribe)
        #     print(ecsobj.ecsComment)
        # address = AddressName.objects.all()
        #
        # for line in address:
        #     print(line.addressName)
        #     print(line.addressIP)
        #     print(line.aaddressComment)
