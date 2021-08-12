import datetime
import random
import time

import redis
import requests




# 验证码随机
def create_code(nums):
    string = ''
    for x in range(nums):
        string += str(random.randint(0,9))
    return string


# 发送验证码
def send_sms(phone):
    url = 'https://gyytz.market.alicloudapi.com/sms/smsSend'
    code = create_code(6)
    # decode_responses = True  这样写存的数据是字符串格式
    re = redis.Redis(decode_responses=True)
    re.set(phone, code, ex=2000)

    # header是阿里云调用接口的时候校验身份的
    header = {'Authorization':'APPCODE ' + 'fea5c18ea0714b04b7ddd89ac405e817'}
    data = {
        'mobile': phone,
        # 审核严格，没有线上已经备案过的项目，一般过不了
        'smsSignId': '2e65b1bb3d054466b82f0c9d125465e2',
        'templateId': '908e94ccf08b4476ba6c876d13f084ad',
        'param': '**code**:' + code + ',**minute**:10'
    }
    result = requests.post(url, headers=header, data=data)
    return result

