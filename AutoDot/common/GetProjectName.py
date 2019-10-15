# coding:utf-8
__author__ = 'GRUNMI'


import os
from common.LogOutput import Log


PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def get_project_name():
    mylogger = Log().get_logger()
    mylogger.info("------------------------------------------------------------------")
    mylogger.info("当前运行文件：{}".format(__file__))
    caseFolder = PATH("../case")
    # 判断是否存在caseFolder文件夹
    if not os.path.exists(caseFolder):
        mylogger.info("不存在项目")
    else:
        for root, dirs, files in os.walk(caseFolder):
            if not files:
                mylogger.info("{}文件下的不存在用例文件".format(caseFolder))
                break
            else:
                mylogger.info("{}文件下的用例文件 {}".format(caseFolder, files))
                projectName = []
                # 去掉 .xlsx 后缀，添加到projectName中
                for name in files:
                    projectName.append(name[:-5])
                return projectName

if __name__ == '__main__':
    projectName = get_project_name()
    print(projectName)


