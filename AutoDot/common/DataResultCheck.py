# coding:utf-8
__author__ = 'GRUNMI'

import re
def data_result_check(Except,checkPoint,response):
    checkPointValue = []
    if checkPoint:
        for i in checkPoint.split(","):
            checkPointValue.append(i)
    ExceptCheckValue = {}
    responseCheckValue = {}
    for value in checkPointValue:
        pattern = "'{}': '(.*?)'".format(value)
        ExceptResult = re.compile(pattern).findall(Except)
        if not ExceptResult:
            pattern ="'{}':'(.*?)'".format(value)
            ExceptResult = re.compile(pattern).findall(Except)
        if not ExceptResult:
            pattern = "'{}': (\d+)".format(value)
            ExceptResult = re.compile(pattern).findall(Except)
        if not ExceptResult:
            pattern = "'{}':(\d+)".format(value)
            ExceptResult = re.compile(pattern).findall(Except)
        ExceptCheckValue.update({value:ExceptResult})

        pattern = "'{}': '(.*?)'".format(value)
        responseResult = re.compile(pattern).findall(response)
        if not responseResult:
            pattern = "'{}':'(.*?)'".format(value)
            responseResult = re.compile(pattern).findall(response)
        if not responseResult:
            pattern = "'{}': (\d+)".format(value)
            responseResult = re.compile(pattern).findall(response)
        if not responseResult:
            pattern = "'{}':(\d+)".format(value)
            responseResult = re.compile(pattern).findall(response)
        responseCheckValue.update({value: responseResult})
    print(ExceptCheckValue)
    print(responseCheckValue)
    if ExceptCheckValue == responseCheckValue:
        print("success")
    else:
        print("failed")
    return ExceptCheckValue, responseCheckValue
if __name__ == '__main__':
    Except = "{'data':[{'name': 15,},{'name': 12}]}"
    checkPoint = "name"
    response = "{'name':13}"
    data_result_check(Except, checkPoint, response)