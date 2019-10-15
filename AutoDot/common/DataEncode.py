# coding:utf-8
__author__ = 'GRUNMI'


from urllib.parse import urlencode

def data_encode(old_data):
    if old_data == "":
        return None
    else:
        if '&' in old_data and '=' in old_data:
            new_data = {}
            for data in old_data.split('&'):
                result = [data.strip() for data in data.split('=')]
                new_data.update(dict([result]))
            return urlencode(new_data)
        elif '&' not in old_data and '=' in old_data:
            new_data = {}
            result = [data.strip() for data in old_data.split('=')]
            new_data.update(dict([result]))
            return urlencode(new_data)
        else:
            data = eval(old_data)
            # （）不编码
            new_data = urlencode(data, safe="()")
            return new_data

if __name__ == '__main__':
    a = data_encode('{"mysql": "1","data":"3"}')
    print(a)
    b = data_encode("{'hahha':{'name':'1','score':'3'}}")
    from urllib.parse import unquote
    print(b)
    print(unquote(b))