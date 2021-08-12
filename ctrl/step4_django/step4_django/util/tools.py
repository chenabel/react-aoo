import json
import uuid

import redis
from django.forms import model_to_dict
from django.http import HttpResponse


def ajax_error(errmsg='',errcode=1):
    data={
        'errcode':errcode,
        'errmsg':errmsg
    }
    response=HttpResponse(json.dumps(data))
    response.__setitem__('Access-Control-Allow-Origin','*')
    return response

def ajax_success(key=None,value=None):
    data={
        'errcode':0,
        'errmsg':'ok'
    }
    if key is not None and value is not  None:
        data[key]=value

    if key is not  None and value is None and isinstance(key,dict):
        for k in key:
            data[k]=key[k]
    response=HttpResponse(json.dumps(data))
    response.__setitem__('Access-Control-Allow-Origin','*')
    return response

def create_token():
    return str(uuid.uuid4())


def redis_save_user(token,user):
    redis_client = redis.Redis()
    user = model_to_dict(user)
    redis_client.set(token, json.dumps(user), ex=7000)

def redis_get(key,is_dict=True):
    redis_client = redis.Redis()
    obj = redis_client.get(key)
    if obj is None:
        return None
    if is_dict:
        return json.loads(obj)
    return obj