# coding:utf-8
__author__ = 'GRUNMI'


from common.ConfigFile import Config

def sql_run(projectName):
    Config(projectName).get_all()