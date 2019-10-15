# coding:utf-8
__author__ = 'GRUNMI'

# 保存动态数据
from common.DataDict import data_dict
import re
from common.LogOutput import Log


mylogger = Log().get_logger()
mylogger.info('当前运行文件：{}'.format(__file__))


def save_dynamic_data(expect,transmitID,transmitTargetID):
    data = {}
    transmitID_value = []
    transmitTargetID_value = []

    # expect转成dict
    expect_dict = data_dict(expect)
    # if expect_dict == None:
    #     return '响应结果不能为空'
    # transmitID转成list
    for i in transmitID.split(","):
        transmitID_value.append(i)

    # transmitTargetID转成list
    for i in transmitTargetID.split(","):
        transmitTargetID_value.append(i)

    # transmitID_value的数量必须与transmitTargetID_value相等
    if len(transmitID_value) == len(transmitTargetID_value):
        num = len(transmitID_value)
        for index in range(num):
            patter = "'{}': '(.*?)'".format(transmitID_value[index]) or "'{}':'(.*?)'".format(transmitID_value[index])
            # print(patter)
            # print(expect_dict)
            transmitID_value_list = re.compile(patter).findall(str(expect_dict))
            # print(transmitID_value_list)
            # re匹配出来的是一个list
            if transmitID_value_list:
                # print([transmitTargetID_value[index],transmitID_value_list[0]])
                # data.update(dict([])) 里面是一个迭代器[],()
                data.update(dict([[transmitTargetID_value[index],transmitID_value_list[0]]]))

            else:
                mylogger.info("{}中不存在 {} 字段".format(expect_dict,transmitID_value[index]))
    # else:
    #     return '动态参数数据数量不相等，请检查数据'
    mylogger.info("更新之后的data：{}".format(data))
    return data

if __name__ == '__main__':
    # expect = "{'1': '4', '2': 5, '3': {'23': '23', '1': [{'67': '2323'}, {'45': '23245'}]}}"
    # transmitID = "1"
    # transmitTargetID = "5"
    # save_dynamic_data(expect, transmitID, transmitTargetID)
    expect = '{"host":"value1121212122"}'
    transmitID = '2'
    transmitTargetID = 'hhh'
    aa = save_dynamic_data(expect, transmitID, transmitTargetID)
    print(aa)