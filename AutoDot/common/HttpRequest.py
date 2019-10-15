# coding:utf-8
__author__ = 'GRUNMI'

import requests
from common.LogOutput import Log


class HttpRequest:
    mylogger = Log().get_logger()
    mylogger.info("------------------------------------------------------------------")
    mylogger.info("当前运行文件：{}".format(__file__))

    def __get(self, url, params=None, **kwargs):
        return requests.get(url, params=params, **kwargs)

    def __post(self, url, headers=None, data=None, **kwargs):
        return requests.post(url, headers=headers, data=data, **kwargs)

    def send_request(self, url, method, headers, data=None, **kwargs):
        if method.lower() == "get":
            self.mylogger.info("运行“get”：{}用例".format(url))
            response = self.__get(url=url, params=data, verify=False, **kwargs)
            response.encoding = 'utf-8'
            self.mylogger.info("{}运行的结果：{}".format(url, response.text))
            return response
        elif method.lower() == "post":
            self.mylogger.info("运行“post”：{}用例".format(url))
            response = self.__post(url=url, headers=headers, data=data, verify=False, **kwargs)
            response.encoding = 'utf=8'
            self.mylogger.info("{}运行的结果：{}".format(url, response.text))
            return response

