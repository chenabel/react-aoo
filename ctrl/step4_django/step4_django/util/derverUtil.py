import random

from django.forms import model_to_dict


def codeString():
    string = ''
    for i in range(0, 6):
        a = random.randint(0, 9)
        string = string + str(a)
    return string

def returnJsonData(list):
    arr = []
    for x in list:
        x = model_to_dict(x)
        for k in x.keys():
            if type(x[k]) == 'time' or type(x[k] == 'datetime'):
                x[k] = str(x[k])
        arr.append(x)
    return arr
