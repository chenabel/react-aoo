import base64
import datetime
import json
import os
import random

import pinyin
import redis
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse, QueryDict
import requests

from company.models import StateData, Menu
from driverSmall import models
from userSmall import models as userModel

from driverSmall.models import DriverInfo

from step4_django.dto.jsonMsg import jsonMsg
from step4_django.settings import BASE_DIR
from step4_django.util.derverUtil import codeString, returnJsonData
from step4_django.util.redis import driverRedisTools
from userSmall.models import UserInfo, OrderInfo

appkey = '203915958'
appSecret = 'h3igz1WORv34lUUmOPUq75QM1o50AHPB'
appCode = '424840c771a54a8cb4f9a62ae4152d90'
appid = 'wx75e53db15a0e1dd6'
AppSecret = '94fdafabc42c562e2ac9d92ec5882f7a'


'''
方立宇代码
'''
def driver(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    state_id = reqObj.get("state_id")
    type_id = reqObj.get("type_id")
    time1 = reqObj.get("time1")
    time2 = reqObj.get("time2")
    input3 = reqObj.get("input3")
    end = reqObj.get("end")
    start = reqObj.get("start")



    DriverArr = DriverInfo.objects.all()
    jm.msgnums = len(DriverArr)

    if state_id:
        DriverArr = DriverArr.filter(
            Q(driver_state__icontains=state_id)
        )
        jm.msgnums = len(DriverArr)
    if type_id:
        DriverArr = DriverArr.filter(
            Q(driver_type__icontains=type_id)
        )
        jm.msgnums = len(DriverArr)

    if time1:
        DriverArr = DriverArr.filter(
            Q(driver_registtime__gte=time1)
        )
        jm.msgnums = len(DriverArr)

    if time2:
        dt = datetime.datetime.strptime(time2, "%Y-%m-%d")
        out_date = (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if out_date:
            DriverArr = DriverArr.filter(
                Q(driver_registtime__lte=out_date)
            )
            jm.msgnums = len(DriverArr)
    if input3!="" and input3 is not None:
        DriverArr = DriverArr.filter(
            Q(driver_tel__icontains=input3)
        )
        jm.msgnums = len(DriverArr)

    DriverArr=DriverArr[int(start):int(end)]
    for item in range(len(DriverArr)):
        a = model_to_dict(DriverArr[item])
        a['driver_registtime'] = str(a['driver_registtime'])
        a['driver_registtime'] = a['driver_registtime'][0:19]
        type = a['driver_type']
        type_name = StateData.objects.get(state_id=type).state_name
        a['type_name'] = type_name
        state = a['driver_state']
        state_name = StateData.objects.get(state_id=state).state_name
        a['state_name'] = state_name

        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


#审核
def driverState(request):
    reqObj = json.loads(request.body)
    driver_id = reqObj.get("driver_id")
    driver = DriverInfo.objects.get(driver_id=driver_id)
    driver.driver_state = 8
    driver.save()
    jm=jsonMsg()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

#锁定
def LockState(request):
    reqObj = json.loads(request.body)
    driver_id = reqObj.get("driver_id")
    driver = DriverInfo.objects.get(driver_id=driver_id)
    driver.driver_state = 9
    driver.save()
    jm=jsonMsg()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

#解锁
def UnlockState(request):
    reqObj = json.loads(request.body)
    driver_id = reqObj.get("driver_id")
    driver = DriverInfo.objects.get(driver_id=driver_id)
    driver.driver_state = 8
    driver.save()
    jm=jsonMsg()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

#获取司机状态
def getState(request):
    reqObj = json.loads(request.body)
    jm=jsonMsg()
    state_type = reqObj.get("state_type")
    StateDataArr=StateData.objects.filter(state_type=state_type)
    for i in range(len(StateDataArr)):
        a = model_to_dict(StateDataArr[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

#获取司机类型
def getType(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    state_type = reqObj.get("state_type")
    StateDataArr = StateData.objects.filter(state_type=state_type)
    for i in range(len(StateDataArr)):
        a = model_to_dict(StateDataArr[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

#获取菜单
def getMethods(request):
    reqObj = json.loads(request.body)
    jm=jsonMsg()
    id = reqObj.get("id")
    MenuArr = Menu.objects.filter(role_id=id)
    for i in range(len(MenuArr)):
        a = model_to_dict(MenuArr[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

#获取数据id
def DetailId(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    driver_id = reqObj.get("driver_id")
    DriverArr = DriverInfo.objects.filter(driver_id=driver_id)
    for item in range(len(DriverArr)):
        a = model_to_dict(DriverArr[item])
        a['driver_registtime'] = str(a['driver_registtime'])
        a['driver_registtime'] = a['driver_registtime'][0:19]
        stateid=a['driver_havecar']
        type_name = StateData.objects.get(state_id=stateid).state_name
        a['type_name'] = type_name
        jm.datas.append(a)


    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

#获取司机订单
def getDriverOrder(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    driver_id=reqObj.get("driver_id")
    state_id=reqObj.get("state_id")
    end = reqObj.get("end")
    start = reqObj.get("start")

    prePage = reqObj.get("prePage")
    currentPage = reqObj.get("currentPage")

    orderInfoArr = OrderInfo.objects.filter(driver_id=driver_id)
    jm.msgnums = len(orderInfoArr)

    if state_id:
        orderInfoArr = orderInfoArr.filter(
            Q(order_state__icontains=state_id)
        )
        jm.msgnums = len(orderInfoArr)
    orderInfoArr = orderInfoArr[int(start):int(end)]
    for i in range(len(orderInfoArr)):
        a = model_to_dict(orderInfoArr[i])

        a['order_starttime'] = str(a['order_starttime'])
        a['order_starttime'] = a['order_starttime'][0:19]

        a['order_desttime'] = str(a['order_desttime'])
        a['order_desttime'] = a['order_desttime'][0:19]

        userid = a['user_id']
        user_name = UserInfo.objects.get(user_id=userid).user_nickname
        a['user_name'] = user_name

        driverid = a['driver_id']
        driver_name = DriverInfo.objects.get(driver_id=driverid).driver_name
        a['driver_name'] = driver_name

        state = a['order_state']
        state_name = StateData.objects.get(state_id=state).state_name
        a['state_name'] = state_name

        type = a['order_type']
        type_name = StateData.objects.get(state_id=type).state_name
        a['type_name'] = type_name

        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")
'''
陈炳祥代码
'''

def getsessionKey(request):
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + AppSecret + '&js_code=' + request.GET.get(
        'code') + '&grant_type=authorization_code'
    data = json.loads(requests.get(url).text)
    js = {}
    js['session_key'] = data['session_key']
    js['openid'] = data['openid']
    return HttpResponse(json.dumps(js, ensure_ascii=False), content_type="application/json")


def driverGetCode(request):
    js = {}
    data = json.loads(request.body)
    url = 'https://gyytz.market.alicloudapi.com/sms/smsSend'
    code = codeString()  # 创建6位数的code
    re = redis.Redis(decode_responses=True)  # 实力化redis
    re.set(data['telNum'], code, ex=300)  # 存入redis
    data = {
        'mobile': str(data['telNum']),
        'smsSignId': '2e65b1bb3d054466b82f0c9d125465e2',
        'templateId': '908e94ccf08b4476ba6c876d13f084ad',
        'param': '**code**:' + str(code) + ',**minute**:3'
    }
    result = requests.post(url, headers={'Authorization': 'APPCODE ' + 'fea5c18ea0714b04b7ddd89ac405e817'}, data=data)
    if result.status_code != 200:
        js['msg'] = '服务器繁忙！'
        js['type'] = "error"
    else:
        js['msg'] = '短信验证码发送成功'
        js['type'] = 'success'
    return HttpResponse(json.dumps(js, ensure_ascii=False), content_type="application/json")


def verificationCode(res):
    jm = jsonMsg()
    data = json.loads(res.body)
    code = driverRedisTools().selectRedis(data['telNum'])  # 得到这个用户的验证码
    if data['code'] == code:
        jm.msg = '注册成功'
        jm.type = 'success'
        try:
            driverModel = DriverInfo.objects.get(driver_tel=data['telNum'])
            jm.msg = '电话号码已使用'
            jm.type = 'error'
            return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type='application/json')
        except:
            driverModel = DriverInfo()
            driverModel.driver_tel = data['telNum']
            driverModel.driver_havecar = data['driverCarType']
            driverModel.driver_city_name = data['cityName']
            driverModel.driver_mini_openid = data['openId']
            driverModel.save()
            jm.msg = '注册成功！'
            jm.type = 'success'
    if code == '' or code == None or data['code'] != code:
        jm.msg = '验证码失效'
        jm.type = 'error'
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type='application/json')


def getDriverPhoto(res):
    jm = {}
    file = res.FILES.get('file')
    file2 = res.FILES['file']
    token = res.POST.get('token')
    name = res.POST.get('type')
    fileName = token + "-" + name + '.' + 'JPG'
    try:
        f = open('/driverSmall/driverFile/' + fileName)
        f.close()
    except IOError:
        f = open(os.path.join(BASE_DIR, 'driverSmall/driverFile', fileName), 'wb')
        for chunk in file2.chunks():
            f.write(chunk)
        jm['msg'] = '上传成功'
        jm['type'] = 'success'
        jm['urlPath'] = os.path.join(BASE_DIR, 'driverSmall/driverFile', fileName)
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def getDriverData(res):
    jm = {}
    data = json.loads(res.body)
    getTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    realTime = str((getTime).split('.')[0])
    driver = DriverInfo.objects.get(driver_tel=data['driverTel'])
    driver.driver_name = data['name']
    driver.driver_idcard_up = data['idPhotoUp'] + '.jpg'
    driver.driver_idcard_down = data['idPhotoDown'] + '.jpg'
    driver.driver_license = data['carPhoto'] + '.jpg'
    driver.driver_plate = data['carNum']
    driver.driver_idcard = data['driverId']
    driver.driver_carcolor = data['color']
    driver.driver_carbrand = data['brand']
    driver.driver_registtime = realTime
    driver.driver_cartype = data['model']
    driver.driver_state = 7
    driver.driver_type = 1
    driver.save()
    jm['type'] = 'none'
    jm['title'] = '请耐心等待审核'
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def getDriverAllOrder(res):
    jm = {
        "allOrder": []
    }
    data = json.loads(res.body)
    allOrder = []
    if data['type'] == 'rightNow':
        allOrder = userModel.OrderInfo.objects.filter((Q(order_type=1) | Q(order_type=2) | Q(order_type=4) | Q(order_type=5)) & Q(order_state=12))
    if data['type'] == 'sunFen':
        allOrder = userModel.OrderInfo.objects.filter(order_type=data['state'],order_state=12)
    if len(allOrder) == 0:
        return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')
    arr = returnJsonData(allOrder)
    for x in range(len(arr)):
        arr[x]['order_starttime'] = str(arr[x]['order_starttime']).split(' ')[1].split('+')[0]
        arr[x]['order_distance'] = int(arr[x]['order_distance']) / 1000
    jm['oid'] = arr[len(arr)-1]['order_id']
    jm['allOrder'] = arr
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def getDriverOrder(res):
    jm = {}
    order = json.loads(res.body)
    oid = str(order['oid'])
    openid = str(order['openid'])
    driver = DriverInfo.objects.get(driver_mini_openid=openid)
    data = userModel.OrderInfo.objects.get(order_id=oid)
    data.driver_id = driver.driver_id
    if data.order_state == 19:
        jm['msg'] = '用户已取消订单'
        jm['type'] = 'error'
        return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')
    else:
        data.order_state = 13
        jm['msg'] = '接单成功'
        jm['type'] = 'success'
        data.save()
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')

def selectDriverOpenid(res):
    openid = res.GET.get('openid')
    jm = {}
    try:
        driverData = DriverInfo.objects.get(driver_mini_openid=openid)
        # 如果司机的账号还未审核 就去请耐心等待审核的页面
        if driverData.driver_state == 7:
            jm['type'] = 'error'
            jm['location'] = "pages/showWatting/showWatting"
        # 如果司机的账号状态等于 正常 就去订单大厅
        if driverData.driver_state == 8:
            jm['type'] = 'success'
            jm['location'] = "pages/orderHall/orderHall"
        if driverData.driver_state == None:
            jm['type'] = 'error'
            jm['location'] = "pages/tipPages/tipPages"
    except:
        jm['type'] = 'error'
        jm['location'] = "pages/index/index"
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def getOrderInfo(res):
    jm = {}
    data = json.loads(res.body)
    orderInfo = userModel.OrderInfo.objects.get(order_id=data['orderId'])
    jm['orderTel'] = orderInfo.order_tel[7:11]
    arr = []
    arr.append(orderInfo)
    orderInfo = returnJsonData(arr)
    orderInfo[0]['order_starttime'] = str(orderInfo[0]['order_starttime'])
    orderInfo[0]['order_distance'] = str(int(orderInfo[0]['order_distance']) / 1000)
    jm['orderInfo'] = orderInfo[0]
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def changeOrder(res):
    jm = {}
    data = json.loads(res.body)
    orderInfo = userModel.OrderInfo.objects.get(order_id=data['oid'])
    getTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    if data['type'] == "getUser":
        orderInfo.order_state = 14
        jm['type'] = 'success'
        jm['msg'] = "操作成功！"
    if data['type'] == "outUser":
        orderInfo.order_state = 15
        orderInfo.order_desttime = getTime
        jm['type'] = 'success'
        jm['msg'] = "操作成功！"
    orderInfo.save()
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def orderPageGetOrder(req):
    jm = {}
    data = json.loads(req.body)
    order = userModel.OrderInfo.objects.get(order_id=data['oid'])
    model = model_to_dict(order)
    model['order_desttime'] = str(model['order_desttime']).split('+')[0]
    model['order_starttime'] = str(model['order_starttime']).split('+')[0]
    jm['order'] = model
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def getDriverOverOrder(req):
    jm = {
        "servicePoints":0
    }
    data = json.loads(req.body)
    driver = DriverInfo.objects.get(driver_mini_openid=data['did'])

    order = userModel.OrderInfo.objects.filter(driver_id=driver.driver_id)
    order = returnJsonData(order)
    today = datetime.date.today()
    getTime = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    day = getTime.split('-')[2].split(' ')[0]
    orderLen = 0
    money = 0
    totalMileage = 0
    servicePoints = 0
    evaluatedLen = 0
    for x in range(len(order)):
        orderDay = str(order[x]['order_starttime']).split('-')[2].split(' ')[0]
        if orderDay == day:
            orderLen += 1
            if order[x]['order_state'] == '16':
                money += float(order[x]['order_price'])
        totalMileage += int(order[x]['order_distance']) / 1000
        comments = userModel.Comments.objects.filter(order_id=order[x]["order_id"])
        comments = returnJsonData(comments)
        if comments != None and comments != []:
            servicePoints += float(comments[0]['comments_level'])
            evaluatedLen += 1
    jm['servicePoints'] = round(servicePoints / evaluatedLen,3)
    jm['money'] = str(money) + '元'
    jm['orderLen'] = orderLen
    jm['totalMileage'] = round(totalMileage,3)
    driver.driver_registtime = str(driver.driver_registtime)
    jm['driver'] = model_to_dict(driver)
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def isDriverOrder(req):
    jm = {}
    data = json.loads(req.body)
    driver = DriverInfo.objects.get(driver_mini_openid=data['openid'])
    order = userModel.OrderInfo.objects.filter(driver_id=driver.driver_id)
    order = returnJsonData(order)
    for x in range(len(order)):
        if order[x]['order_state'] == 14:
            order[x]['order_starttime'] = str(order[x]['order_starttime'])
            order[x]['order_desttime'] = str(order[x]['order_desttime'])
            jm['order'] = order[x]
    if jm == "" or jm == None:
        jm['flage'] = True
    else:
        jm['flage'] = False
    return HttpResponse(json.dumps(jm,ensure_ascii=False),content_type='application/json')


def getMyOrder(req):
    jm = {}
    data = json.loads(req.body)
    driver = DriverInfo.objects.get(driver_mini_openid=data['openId'])
    driver = model_to_dict(driver)
    order = userModel.OrderInfo.objects.filter(driver_id=driver['driver_id'])
    model = returnJsonData(order)
    for x in range(len(model)):
        model[x]['order_starttime'] = str(model[x]['order_starttime']).split("+")[0]
        state = StateData.objects.get(state_id=model[x]['order_state'])
        print(model[x]['order_state'])
        print(type(model[x]['order_state']))
        state = model_to_dict(state)
        if model[x]['order_state'] == '15':
            model[x]['order_state'] = '等待顾客支付'
        if model[x]['order_state'] == '13':
            model[x]['order_state'] = '正在进行中'
        if model[x]['order_state'] == '14':
            model[x]['order_state'] = '正在进行中'
        if model[x]['order_state'] == '16':
            model[x]['order_state'] = '已支付'
        if model[x]['order_state'] == '18':
            model[x]['order_state'] = '已评价'
        if model[x]['order_state'] == '17':
            model[x]['order_state'] = '未评价'
        if model[x]['order_state'] == '19':
            model[x]['order_state'] = '用户已取消'
	# model[x]['order_state'] = state['state_name']
        # model[x]['order_startadd'] = model[x]['order_startadd'].split("市")[1]
        # model[x]['order_destadd'] = model[x]['order_destadd'].split("市")[1]
        model[x]['order_starttime'] = str(model[x]['order_starttime'])
        model[x]['order_desttime'] = str(model[x]['order_desttime'])
    jm['driver'] = model
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')


def getDriverMoney(req):
    jm={}
    data = json.loads(req.body)
    driverData = DriverInfo.objects.get(driver_mini_openid=data['did'])
    driverData = model_to_dict(driverData)
    jm['money'] = driverData['driver_money']
    return HttpResponse(json.dumps(jm, ensure_ascii=False), content_type='application/json')

def getDerverLicense(req):
    jm = {}
    fileName = '/driverSmall/driverFile/o0_e95UFs2bI9kHKs2pRHqWBJURk-驾驶证照片.JPG'
    path = BASE_DIR
    # fileAdd=os.path.join(f'{path}'+fileName)
    fileList = open(os.path.join(f'{path}'+fileName), 'rb')
    # strToImage(fileAdd)
    jm['img'] = base64.b64encode(fileList.read())
    # tu_b = base64.b64decode(jm['img'])
    # with open('tu.png', 'wb') as fp:
    #     fp.write(tu_b)
    # jm['image'] = fp
    # image = ImageCaptcha()
    # image.generate(jm['img'])
    # image.show()
    # captcha_list = self.get_captcha()  # 返回一个列表
    # captcha_str = ''.join(captcha_list)  # 将列表的所有内容整合成一个字符串
    # captcha_image = image.generate(captcha_str)
    return HttpResponse(jm['img'], content_type="image/png")


def strToImage(str,filename):
    image_str= str.encode('ascii')
    image_byte = base64.b64decode(image_str)
    image_json = open(filename, 'wb')
    image_json.write(image_byte)  #将图片存到当前文件的fileimage文件中
    image_json.close()
