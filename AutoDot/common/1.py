# coding:utf-8
__author__ = 'GRUNMI'


a = [12,123]
print(a[0])
for i in a:
    print(i)
if a.count(12,):
    print(12121212)
else:
    print(21122121)


b=[('host', 'host1')]
print(dict(b))


for i,y in dict(b).items():
    print(i,y)



a = {'1':'2','2':1,"3":{"23":"23","1":[{"67":"2323"},{"45":"23245"}]}}
# if '23' in a:
#     print('sdsddfsfs')
if str(a).count("4"):
    print("wefergfdgfgf")
b = "1,2"
print(list(b))
c = {'1':4,'2':5}
for i in b.split(","):
    a[i]=c[i]
print(a)

# w=[]
# print(len(str(w[0])))
# if len(str(w[0]))>0:
#     print(9876543)
import re
data = {'name': 'replaceID_after_value', 'score': 'score_value'}
patter = "'{}': '(.*?)'".format('name1')
be_replace_value_list = re.compile(patter).findall(str(data))
print(be_replace_value_list)

ad = {"name":23}
abb = {"age":44}
abb.update(ad)
print(abb)
a = str(["1",'3',24,54])
a.replace('"',"'")
print(a)

v = {"1":2}
if v:
    print(11)
else:
    print(222)


d = [1,2,3,4,5,3]
for i in d[::-1]:
    print(i)


u ="场景报告2018-10-09 15-37-24.xlsx"
if u.find("场景报告")>=0:
    print(u)
else:
    print(876543)


x = '1,23,45,67,'
id = []
for i in x.split(','):
    id.append(i)
print(id)
print(id[:-1])
print(type(id))
iii=float(1.0)
print(type(iii),iii)
www = int(iii)
print(type(www), www)


dic = [{"id":"1"},{"id":2}]
case_id = []
for i in dic:
    case_id.append(int(i["id"]))

print(case_id)
cccc = [1,2,3]
print(set(case_id)<=set(cccc))

result = {"projectname": 1212}
report = [{"name":2}]
result.update({"name": report})
print(result)

