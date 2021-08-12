import json
import uuid

import redis
from django.forms import model_to_dict


def redisSaveEmployeeInfo(employeeInfo,listname):
    re = redis.Redis(decode_responses=True)
    token = str(uuid.uuid4())
    value={token:json.dumps(employeeInfo)}
    re.lpush(listname,json.dumps(value))
    return token
def redisGetEmployeeInfo(listname):
    re = redis.Redis(decode_responses=True)
    info=re.lrange(listname,0,-1)
    return info
def deleteEmployeeInfo(listname,token):
    info=redisGetEmployeeInfo(listname)
    for i in range(len(info)):
        employeeinfo=json.loads(info[i])
        if token in employeeinfo.keys():
            re = redis.Redis(decode_responses=True)
            content=re.lindex(listname,i)
            re.lrem(listname,value=content,num=0)
def updateEmployeeInfo(listname,token,employeeInfo):
    info = redisGetEmployeeInfo(listname)
    for i in range(len(info)):
        employeeinfo = json.loads(info[i])
        if token in employeeinfo.keys():
            re = redis.Redis(decode_responses=True)
            content = re.lindex(listname, i)
            re.lrem(listname, value=content, num=0)
            value = {token: json.dumps(employeeInfo)}
            re.lpush(listname, json.dumps(value))
def redisSaveUserInfo(userinfo):
    re = redis.Redis(decode_responses=True)
    token = str(uuid.uuid4())
    re.set(token, json.dumps(userinfo), ex=7000)
    return token
def redis_save_user(token,user):
    redis_client = redis.Redis()
    user = model_to_dict(user)
    redis_client.set(token, json.dumps(user), ex=7000)
def redis_get(key, is_dict = True):
    redis_client = redis.Redis()
    obj = redis_client.get(key)
    print(obj)
    if obj is None:
        return
    if is_dict:
        return json.loads(obj)
    return obj
class driverRedisTools:
    # ip 地址 访问哪个ip 的redis
    __host = '127.0.0.1'
    # 端口号 获得端口号
    __post = '6379'
    def inputRedis(self, key, value, relTime=7200):
        rs = redis.StrictRedis(host=driverRedisTools.__host, port=driverRedisTools.__post, db=0)  # 数据库0
        rs.set(key, json.dumps(value), ex=relTime)  # 存入数据库
        print('我是存入redis数据库的操作成功信息，看到我等于看到存入redis成功啦！')

    def selectRedis(self, key):
        rs = redis.StrictRedis(host=driverRedisTools.__host, port=driverRedisTools.__post, db=0, decode_responses=True)  # 数据库0
        print('这是你去key:',key)
        data = rs.get(key)
        if data != None and data != '':
            print(f'这是你通过 {key} 拿到的值: {data}')
            return data
        else:
            print('这个key 没有对应的值，可能是key不存在或者是key的值为空')
            return False