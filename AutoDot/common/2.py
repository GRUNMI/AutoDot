# coding:utf-8
__author__ = 'GRUNMI'


import ast

a = "{'c':2}"
b = "1"
print(ast.literal_eval(a), type(ast.literal_eval(a)))


c = {"1":3,"4":"6"}
d = {"4":"6","1":3}
if c == d:
    print(12121)

import pandas as pd
import os

excel_data = pd.read_excel("test.xlsx")
print(excel_data)
print("excel_data",os.linesep,excel_data)
data = excel_data.to_dict(orient='records')
print(data)
