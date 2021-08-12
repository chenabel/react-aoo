import hashlib
import time

import requests
import xmltodict
from django.http import HttpResponse

from step4_django.util.wechatTool import wechatTool

to_user=''
from_user='gh_3405350ec2a6'
def initMenu(request):
    accesstoken=wechatTool().getToken()
    url=' https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+accesstoken
    data='''
{
     "button":[
     {	
          "type":"view",
           "name":"我要打车",
           "url":"http://120.77.80.155"
      },
      {	
          "type":"view",
          "name":"DiDi Park",
          "url":"http://120.77.80.155"
      },
      {
           "name":"滴滴服务",
           "sub_button":[
           {
               "type":"view",
               "name":"司机招募",
               "url":"http://120.77.80.155"
            },
            {
               "type":"view",
               "name":"在线客服",
               "url":"http://120.77.80.155"
            }]
       }]
 }
    '''
    result=requests.post(url,data=data.encode('utf-8'))
    print(result)
    return HttpResponse('')
def index(req):
    global to_user
    token = 'cbx'
    timestamp = req.GET.get('timestamp')
    nonce = req.GET.get('nonce')
    signature = req.GET.get('signature')
    arr = [token, timestamp, nonce]
    arr.sort()
    string = ''.join(arr)
    string = hashlib.sha1(string.encode('utf-8')).hexdigest()
    echostr = req.GET.get('echostr')
    if string == signature and echostr is not None and echostr!="":
        return HttpResponse(echostr)
    content=xmltodict.parse(req.body)['xml']
    to_user=content['FromUserName']
    print(content)
    if content['MsgType']=='event':
        if content['Event']=='subscribe':
            message='''欢迎来到小滴的世界，在这里将为你打开出行世界的大门！
         
要出门？想打车？↓↓↓点击底部菜单栏【我要打车】

想聊天？想聚会？↓↓↓点击底部菜单栏进入滴粉的秘密基地【DiDi Park】

有疑问？要福利？↓↓↓点击底部菜单栏【滴滴服务】

你想要的这里都有，还有不定期的打车券哟~答应我，三生三世，永不取关。'''
            return _returnMessage(message)	

def _returnMessage(message):
    global to_user,from_user
    returntime=time.time()
    string=f'''
    <xml>
      <ToUserName><![CDATA[{to_user}]]></ToUserName>
      <FromUserName><![CDATA[{from_user}]]></FromUserName>
      <CreateTime>{returntime}</CreateTime>
      <MsgType><![CDATA[text]]></MsgType>
      <Content><![CDATA[{message}]]></Content>
    </xml>
    '''
    return HttpResponse(string)
