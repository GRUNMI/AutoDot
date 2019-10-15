# coding:utf-8
__author__ = 'GRUNMI'


def data_dict(old_data):
    try:
        if old_data == "":
            return None
        else:
            if '&' in old_data and '=' in old_data:
                new_data = {}
                for data in old_data.split('&'):
                    result = [data.strip() for data in data.split('=')]
                    new_data.update(dict([result]))
                return new_data
            elif '&' not in old_data and '=' in old_data:
                new_data = {}
                result = [data.strip() for data in old_data.split('=')]
                new_data.update(dict([result]))
                return new_data
            else:
                new_data = eval(old_data)
                return new_data
    except Exception as e:
        return e


if __name__ == '__main__':
    a = data_dict("name=1&score=3")
    print(a)
    b = data_dict("{'hahha':{'name': '1', 'score': '3'}}")
    print(b)
