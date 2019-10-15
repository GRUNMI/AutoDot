# coding:utf-8
__author__ = 'GRUNMI'

import logging
import os
import time

# 记录日志

logPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

# 判断是否存在文件夹，不存在则创建
if not os.path.exists(logPath):
    os.mkdir(logPath)


class Log():
    def __init__(self):
        self.logger = logging.getLogger()

        # 第二次调用log的时候，根据getLogger(name)里的name获取同一个logger，
        # 而这个logger里已经有了第一次你添加的handler，第二次调用又添加了一个handler，
        # 所以，这个logger里有了两个同样的handler，以此类推，调用几次就会有几个handler


        # 第一种：每次运行之前，移除handler
        # self.logger.removeHandler(handler)

        # 第二种：用pop方法把logger.handlers列表中的handler移除，注意如果你add了多个handler，这里需多次pop，或者可以
        # logger.handlers.pop()


        # 第三种：直接为handlers列表赋空值
        # logger.handler = []

        #  第四种：进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s----  %(message)s')
            handler.setFormatter(formatter)
            # 打印在屏幕上
            self.logger.addHandler(handler)
            self.logFileName = os.path.join(logPath, '%s.log' % time.strftime('%Y_%m_%d'))
            fh = logging.FileHandler(self.logFileName, mode='a', encoding='utf-8')
            fh.setFormatter(formatter)
            # 记录在logs文件夹的logFileName文件中
            self.logger.addHandler(fh)


    def get_logger(self):
        # print(self.logger.handlers)
        return self.logger

if __name__ == '__main__':
    mylogger = Log().get_logger()
    mylogger.debug("test debug")
    mylogger.info("test info")
    mylogger.error('haha')
    mylogger.error('hahha111')
