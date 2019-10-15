# coding:utf-8
__author__ = 'GRUNMI'

import os
from common.LogOutput import Log
import xlrd


class GetCase:
    def __init__(self, projectName):
        PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))
        self.mylogger = Log().get_logger()
        self.mylogger.info("------------------------------------------------------------------")
        self.mylogger.info("当前运行文件：{}".format(__file__))
        self.mylogger.info("准备获取 {} 项目的用例路径".format(projectName))
        self.caseFilePath = PATH("../case/{}.xlsx".format(projectName))
        self.mylogger.info("获取到 {} 项目的用例路径：{}".format(projectName, self.caseFilePath))
        self.projectName = projectName

    def get_project_case(self):
        all_case = []
        try:
            caseFiles = xlrd.open_workbook(self.caseFilePath)
            caseSheet = caseFiles.sheet_by_index(0)
            # 标题在excel用例文件的第一行
            title = caseSheet.row_values(0)
            self.mylogger.info("获取用例的标题：{}".format(title))
            # 获取用例总数量
            case_rows = caseSheet.nrows
            # print(case_rows, type(case_rows))

            # 获取执行用例数量和不执行用例数量
            for index, val in enumerate(caseSheet.row_values(0)):
                if val == 'Run':
                    num = caseSheet.col_values(index)
                    self.noRunNum = num.count('NO')
                    self.runNum = num.count('YES')

            if case_rows > 1:
                for case_row in range(1, case_rows):
                    # 获取case_row行内容
                    case = caseSheet.row_values(case_row)
                    # 当前行内容和用例标题构成字典形式
                    active_row_case = dict(zip(title, case))
                    # 在字典中新增rowid数值，表示用例所在行数
                    active_row_case['RowID'] = case_row+1
                    # 每行用例循环添加到all_case中
                    all_case.append(active_row_case)
                self.mylogger.info("获取 “{}” 所有用例：{}".format(self.projectName, all_case))
                return all_case, case_rows-1, self.caseFilePath, self.projectName, self.noRunNum, self.runNum
            else:
                return all_case, case_rows-1, self.caseFilePath, self.projectName, self.noRunNum, self.runNum

        except Exception as e:
            self.mylogger.info("获取 “{}” 异常，强制结束程序：{}".format(self.projectName, e))
            # exit()
            quit()


if __name__ == '__main__':
    a = GetCase("自动干线").get_project_case()
    print(a)
