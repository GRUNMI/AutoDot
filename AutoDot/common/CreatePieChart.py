# coding:utf-8
__author__ = 'GRUNMI'


import openpyxl
from openpyxl.chart import PieChart, Reference
import xlrd
import os
import common.LogOutput


class CreatePie:
    def __init__(self, projectName, type=0):
        '''
        :type 标识生成测试报告类型 0:项目用例，1：场景用例
        '''
        self.mylogger = common.LogOutput.Log().get_logger()
        self.mylogger.info("------------------------------------------------------------------")
        self.mylogger.info("当前运行文件：{}".format(__file__))

        # 获取用例文件成功、失败、不执行的数量
        self.PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))
        caseFolder = self.PATH("../report") + "\\"+projectName+"\\"+"excelReport"
        for root, dirs, files in os.walk(caseFolder):
            print(files[::])
            # 获取excelReport文件夹中的最后一个文件
            try:
                if files:
                    # for name in files[-1::]:
                        # self.caseFile = os.path.join(caseFolder, name)
                    # 倒序查找
                    for name in files[::-1]:
                        # print(name)
                        # 项目报告
                        if type == 0 and name.find("settingReport") < 0:
                            self.caseFile = os.path.join(caseFolder, name)
                            break
                        # 场景用例报告
                        elif type == 1 and name.find("settingReport") >= 0:
                            self.caseFile = os.path.join(caseFolder, name)
                            break

                    try:
                        wb = xlrd.open_workbook(self.caseFile)
                        ws = wb.sheet_by_index(0)
                        # 获取RunResult里面的值
                        for index, title in enumerate(ws.row_values(0)):
                            if title == 'RunResult':
                                contents = ws.col_values(index)
                                self.noRunNum = contents.count('')
                                self.successNum = contents.count('true')
                                self.failedNum = contents.count('false')

                    except Exception as e:
                        self.mylogger.info("获取 “{}” 异常，强制结束程序：{}".format(self.caseFile, e))
                        # exit()
                        quit()
                else:
                    raise Exception("在excelReport下未找到文件")
            except Exception as e:
                self.mylogger.info(e)
                exit()


    # 生成图表
    def pie(self):
        try:
            self.mylogger.info("准备打开用例文件，准备生成图表")
            wb = openpyxl.load_workbook(self.caseFile)
            self.mylogger.info("成功用例数：{}个，失败用例数：{}个，不执行用例数：{}个 ".format(self.successNum, self.failedNum, self.noRunNum))
            rows = [
                ['结果', '数量'],
                ['成功', self.successNum],
                ['失败', self.failedNum],
                ['不执行', self.noRunNum],
            ]
            ws = wb.create_sheet('casePie')
            # 把值添加在excel中
            for row in rows:
                ws.append(row)

            # 创建图表实例
            chart = PieChart()

            # 设置类别的取值，min_row和max_row有bug，需要加1
            labels = Reference(ws, min_col=1, min_row=2, max_row=5)
            # 设置数据的取值，min_col在哪一行取值
            data = Reference(ws, min_col=2, min_row=1, max_row=4)
            # titles_from_data：鼠标移动上去图表上显示数据
            chart.add_data(data, titles_from_data=True)

            # 设置标题
            chart.title = "用例运行结果图表"
            # 设置类别
            chart.set_categories(labels=labels)
            # 将图表添加在哪个位置
            ws.add_chart(chart, 'D1')

            wb.save(self.caseFile)
            wb.close()
            self.mylogger.info("生成图表完成，保存在{}文件中".format(self.caseFile))
        except Exception as e:
            self.mylogger.debug("出现异常，异常日志：{}".format(e))


if __name__ == '__main__':
    CreatePie('test', type=1).pie()
