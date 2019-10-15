# coding:utf-8
__author__ = 'GRUNMI'


import os
import configparser
from AutoDot.common.LogOutput import Log

PATH = lambda P: os.path.abspath(os.path.join(os.path.dirname(__file__), P))

# cf = configparser.ConfigParser()
# cf.read(PATH("./conf/test.ini"))

# print(cf.sections())
# print(dict(cf._sections))
# dic = dict(cf._sections)
# for i in dic:
#     dic[i] = dict(dic[i])
# print(dic)

#
# print(cf.options("mysql"))
# print(cf.items("mysql"))


mylogger = Log().get_logger()
mylogger.info('当前运行文件：{}'.format(__file__))
# 重新configparser方法，去掉lower()转成小写
class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class Config:
    def __init__(self, projectName):
        # self.cf = configparser.ConfigParser()
        self.cf = MyConfigParser()
        # 路径
        # 配置文件夹路径
        self.cfPath = PATH("../config")
        # 配置文件路径
        self.cfFilePath = PATH("../config/{}.ini").format(projectName)
        if not os.path.exists(self.cfPath):
            os.mkdir(self.cfPath)
            mylogger.info("新建配置文件路径{}".format(self.cfPath))
        if not os.path.exists(self.cfFilePath):
            # 不存在配置文件，则新增空配置文件
            file = open(self.cfFilePath, 'w')
            mylogger.info("新建配置文件{}".format(self.cfFilePath))
            file.close()
        self.cf.read(self.cfFilePath,encoding='utf-8')
        mylogger.info("读取配置文件{}".format(self.cfFilePath))
        self.sections = self.cf.sections()
        mylogger.info("获取配置文件所有sections：{}".format(self.sections))

    def get_all(self):
        all_data = dict(self.cf._sections)
        for i in all_data:
            all_data[i] = dict(all_data[i])
        mylogger.info("获取配置文件所有内容转成字典格式展示：{}".format(all_data))
        return all_data

    def get_section_all_option(self, section_name):
        if not self.sections.count(section_name):
            mylogger.info("获取配置文件section_name：{}，不存在，准备创建section_name {}".format(section_name, section_name))
            self.cf.add_section(section_name)
            with open(self.cfFilePath, "w+") as f:
                self.cf.write(f)
                mylogger.info("新增配置文件section_name：{} 成功".format(section_name))
        else:
            data = dict(self.cf.items(section_name))
            mylogger.info("获取配置文件sections：{} 下的options：{}".format(section_name, data))
            return {section_name: data}

    def get_option_value(self, section_name, option_name):
        # 读取
        if not self.sections.count(section_name):
            mylogger.info("获取配置文件section_name：{}，不存在".format(section_name))
            # print("不存在section_name：{}".format(section_name))
        else:
            mylogger.info("获取配置文件sections：{} 下的options：{}".format(section_name,self.cf.options(section_name)))
            if not self.cf.options(section_name).count(option_name):
                mylogger.info("获取配置文件option_name：{}，不存在".format(option_name))
                # print("不存在option_name：{}".format(option_name))
            else:
                value = self.cf.get(section_name, option_name)
                mylogger.info("获取配置文件section_name：{}，option_name：{}的值为：{}".format(section_name,option_name,value))
                # print(value)
                return value

    def add_option_value(self,section_name,option_name,option_value):
        # 添加新的section，如果存在，则报错
        if not self.sections.count(section_name):
            mylogger.info("获取配置文件section_name：{}，不存在".format(section_name))
            # 添加section
            self.cf.add_section(section_name)
            mylogger.info("准备新增配置文件section_name：{}".format(section_name))
            with open(self.cfFilePath, "w+") as f:
                self.cf.write(f)
                mylogger.info("新增配置文件section_name：{} 成功".format(section_name))
        # 添加/修改 option
        mylogger.info("准备更新配置文件option_name：{}".format(option_name))
        self.cf.set(section_name, option_name, option_value)
        with open(self.cfFilePath, "w+") as f:
            self.cf.write(f)
            mylogger.info("更新完成，配置文件section_name：{}，option_name：{}，option_value：{}".format(section_name,option_name,option_value))

    def add_dict(self, data_dict):
        mylogger.info("准备将{}写入配置文件中".format(data_dict))
        for key in data_dict:
            if not self.cf.sections().count(key):
                self.cf.add_section(key)
            for key1 in data_dict[key]:
                self.cf.set(key,key1,data_dict[key][key1])
        with open(self.cfFilePath, "w+") as f:
            self.cf.write(f)
        mylogger.info("成功将{}更新到配置文件中".format(data_dict))
        # 内部调用
        self.get_all()


    def remove_option(self,section_name,option_name):
        # 删除option
        mylogger.info("准备删除section_name：{}，option_name：{}".format(section_name,option_name))
        if not self.sections.count(section_name):
            mylogger.info("不存在section_name：{}，不需要删除".format(section_name))
            # print("不存在section_name：{}，不需要删除".format(section_name))

        else:
            mylogger.info("获取配置文件sections：{} 下的options：{}".format(section_name, self.cf.options(section_name)))
            if not self.cf.options(section_name).count(option_name):
                mylogger.info("不存在option_name：{}，不需要删除".format(option_name))
                # print("不存在option_name：{}，不需要删除".format(option_name))
            else:
                self.cf.remove_option(section_name, option_name)
                with open(self.cfFilePath, "w+") as f:
                    self.cf.write(f)
                    mylogger.info("删除成功，section_name：{}，option_name：{}".format(section_name,option_name))

    def remove_section(self,section_name):
        # 删除section
        mylogger.info("准备删除section_name：{}".format(section_name))
        if not self.sections.count(section_name):
            mylogger.info("不存在section_name：{}，不需要删除".format(section_name))
            # print("不存在section_name：{}，不需要删除".format(section_name))
        else:
            self.cf.remove_section(section_name)
            with open(self.cfFilePath, "w+") as f:
                self.cf.write(f)
                mylogger.info("删除成功，section_name：{}".format(section_name))
        # 配置文件没有内容，则删除
        if os.path.getsize(self.cfFilePath) == 0:
            os.remove(self.cfFilePath)

if __name__ == '__main__':
    projectName = 'test1'
    # 定义动态数据section  ： changedata
    section_name = 'changeData'
    option_name = 'host'
    option_value = 'value12'
    data_dict = {'mysql': {'host': 'host', 'user': 'user', 'passwd': 'passwd', 'db': 'db', 'port': '3306', 'chaeset': 'utf8'}}
    # Config(projectName=projectName).get_all()
    Config(projectName=projectName).get_section_all_option(section_name=section_name)
    # Config(projectName=projectName).get_option_value(section_name=section_name,option_name=option_name)
    # Config(projectName=projectName).add_option_value(section_name=section_name,option_name=option_name,option_value=option_value)
    # Config(projectName=projectName).add_dict(data_dict=data_dict)
    # Config(projectName=projectName).remove_option(section_name=section_name,option_name=option_name)
    # Config(projectName=projectName).remove_section(section_name=section_name)


