# coding:utf-8
__author__ = 'GRUNMI'
import common.LogOutput
import os
import xlrd


def get_project_run_num(case_name, type):
    '''
    :type 标识生成测试报告类型 0:项目用例报告，1：场景用例报告
    '''
    mylogger = common.LogOutput.Log().get_logger()
    mylogger.info("------------------------------------------------------------------")
    mylogger.info("当前运行文件：{}".format(__file__))

    # 获取用例文件成功、失败、不执行的数量
    PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))
    caseFolder = PATH("../report") + "\\" + case_name + "\\" + "excelReport"
    for root, dirs, files in os.walk(caseFolder):
        # print(files[-1::])
        # 查找最后一个
        # for name in files[-1::]:
        # 倒序查找
        for name in files[::-1]:
            # 项目报告
            if type == 0 and name.find("settingReport") < 0:
                caseFile = os.path.join(caseFolder, name)
                break
            # 场景用例报告
            elif type == 1 and name.find("settingReport") >= 0:
                caseFile = os.path.join(caseFolder, name)
                break
        try:
            print(caseFile)
            wb = xlrd.open_workbook(caseFile)
            ws = wb.sheet_by_index(0)
            # contents = ws.col_values(23)
            for index, val in enumerate(ws.row_values(0)):
                if val == 'RunResult':
                    contents = ws.col_values(index)
                    successNum = contents.count('true')
                    failedNum = contents.count('false')
                    noRunNum = contents.count('')
                    return successNum, failedNum, noRunNum

        except Exception as e:
            mylogger.info("获取 “{}” 异常，强制结束程序：{}".format(caseFile, e))
            # exit()
            quit()


if __name__ == '__main__':
    a = get_project_run_num('test', type=1)
    print(a)