import hashlib


def md5String(val):
    if val==None or type(val)!=type(""):   return "";
    input_name=hashlib.md5()
    input_name.update(val.encode("utf-8"))
    return input_name.hexdigest()