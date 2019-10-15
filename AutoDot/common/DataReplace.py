# coding:utf-8
__author__ = 'GRUNMI'


import re
from common.DataDict import data_dict
from common.LogOutput import Log


mylogger = Log().get_logger()
mylogger.info('当前运行文件：{}'.format(__file__))

def data_replace(data,replace_data,changge_data):

    replace_value = []
    # 需要改变的字段存储在列表中
    if replace_data:
        for i in replace_data.split(","):
            replace_value.append(i)
    mylogger.info("动态字段转化成列表：{}".format(replace_value))

    # 替换data中的动态值
    for value in replace_value:
        if value in changge_data.keys():
            patter = "'{}': '(.*?)'".format(value) or "'{}':'(.*?)'".format(value)
            be_replace_value_list = re.compile(patter).findall(str(data_dict(data)))
            # print(be_replace_value_list)
            # re匹配出来的是一个list
            for be_replace_value in be_replace_value_list:
                data = data.replace(be_replace_value, changge_data[value])
        else:
            mylogger.info("环境配置中不存在 {} 动态字段".format(value))
    mylogger.info("更新之后的data：{}".format(data))
    print(data)
    return data
if __name__ == '__main__':
    data = "name=1"
    replace_data = "name,score"
    changge_data = {'name': 'replaceID_after_value', 'score': 'score_value'}
    data_replace(data,replace_data,changge_data)


    test2 = "{'name': [{'name': 'math', 'score': '90'}, {'name': 'english', 'score': '88'}]}"
    replaceID = "name,score"
    replaceID_after = {'name': 'replaceID_after_value', 'score': 'score_value'}
    data_replace(test2, replaceID, replaceID_after)
