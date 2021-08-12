import redis
import requests


class wechatTool():
    def __init__(self):
        self.appID='wxd7531475943a05b3'
        self.appsecret='2f5cba99f7f1563bbfe56f58544342b9'
        self.time=7000
    def getToken(self):
        re = redis.Redis(decode_responses=True)
        if re.get('accesstoken') is not None and re.get('accesstoken')!="":
            return re.get('accesstoken')
        url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+ self.appID + '&secret=' + self.appsecret
        result=requests.get(url)
        if result.status_code!=200:
            return False
        if 'errcode' in result.json().keys():
            print(result.json()['errmsg'])
            return False
        re.set('accesstoken',result.json()['access_token'],ex=self.time)
        return  result.json()['access_token']