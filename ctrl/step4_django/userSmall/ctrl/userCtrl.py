import datetime
import json

import requests
from django.db.models import Q
from django.http import HttpResponse

from company.models import StateData
from driverSmall.models import DriverInfo
from step4_django.dto.jsonMsg import jsonMsg
from step4_django.util.redis import *

# 用户登录
from userSmall.models import UserInfo, OrderInfo, HistoryPassenge, Comments
from userSmall.util.sms import send_sms


def userLogin(request):
    code = request.GET.get('code')
    userInfo = request.GET.get('userInfo')
    js = jsonMsg()
    appId = 'wx638cff77b89c27c4'
    appSecret = 'd175d2eb37ec3dfa1da35cdc69f0a230'
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appId + '&secret=' + appSecret + '&js_code=' + code + '&grant_type=authorization_code'
    result = requests.get(url)
    if result.status_code != 200:
        js.id = 0
        js.msg = '服务器繁忙'
        return HttpResponse(json.dumps(js.__dict__, ensure_ascii=False), content_type="application/json")
    if 'session_key' not in result.json().keys() or 'openid' not in result.json().keys():
        js.id = -1
        js.msg = '服务器繁忙'
        return HttpResponse(json.dumps(js.__dict__, ensure_ascii=False), content_type="application/json")
    openid = result.json()['openid']
    userArr = UserInfo.objects.filter(user_mini_openid=openid)
    userInfos = json.loads(userInfo)

    # 没有找到用户
    if len(userArr) <= 0:
        user = UserInfo()
        # 存入数据
        user.user_mini_openid = openid
        user.user_nickname = userInfos["nickName"]
        user.user_sex = userInfos["gender"]
        user.user_province = userInfos["province"]
        user.user_city = userInfos["city"]
        user.user_headimgurl = userInfos["avatarUrl"]
        user.user_country = userInfos["country"]
        user.user_state=24
        user.user_registtime = str(datetime.datetime.now())
        token = redisSaveUserInfo(model_to_dict(user))
        user.save()
        js.id = 1

    # 有找到用户
    else:
        user = userArr[0]
        user.user_registtime = str(user.user_registtime)
        token = redisSaveUserInfo(model_to_dict(user))
        js.id = -1
        js.data2 = user.user_tel

    js.datas = {"token": token}
    print(11,js.datas)
    return HttpResponse(json.dumps(js.__dict__, ensure_ascii=False), content_type="application/json")


#  获取uid
def check_is_login(request):
    token = request.GET.get('token')
    if token is None or token == '':
        return False
    user = redis_get(token)
    if user is None or ('user_id' not in user.keys()):
        return False
    uid = user['user_id']
    return uid


# 发送验证码
def sendCode(req):
    jm = jsonMsg()
    #  拿到手机号码
    phone = req.GET.get('phoneNum')
    # 校验手机号码有效性  前后端都要校验
    rs = send_sms(phone)
    if rs.status_code == 200:
        jm.id = 1
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


# 确认验证
def verify(req):
    jm = jsonMsg()
    tel = req.GET.get('phoneNum')
    code = req.GET.get('codeNum')
    token = req.GET.get('token')
    re = redis.Redis(decode_responses=True)
    sysCode = re.get(tel)

    if code != sysCode:
        jm.id = -1
        jm.msg = '验证码输入错误，请重新输入'
    else:
        user = redis_get(token)
        openid = user['user_mini_openid']
        infos = UserInfo.objects.filter(user_mini_openid=openid)[0]
        infos.user_registtime = str(infos.user_registtime)
        infos.user_tel = tel
        infos.save()
        re.set(token, json.dumps(model_to_dict(infos)),ex=7000)
        jm.id = 1
        jm.msg = '手机已绑定'
        jm.datas = {"tel":tel}
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def userOrder(req):
    jm = jsonMsg()
    starttime = req.GET.get('starttime')
    ordertype = req.GET.get('ordertype')
    startAddress = req.GET.get('startAddress')
    endAddress = req.GET.get('endAddress')
    token = req.GET.get('token')
    distance = req.GET.get('distance')
    price = req.GET.get('price')
    re = redis.Redis(decode_responses=True)
    passengerName = req.GET.get('passengerName')
    passengertel = req.GET.get('passengertel')
    infos = re.get(token)

    if infos != None and infos != "":
        uid = json.loads(infos)['user_id']
        orders = OrderInfo.objects.filter(Q(user_id=uid) & Q(order_state=15))
        if len(orders)>0:
            jm.id = 2
            jm.msg = '之前的订单还没支付，跳转到我的行程进行支付'
        else:
            if passengertel != None and passengertel != "":
                order = OrderInfo()
                order.user_id = json.loads(infos)['user_id']
                order.order_startadd = startAddress
                order.order_destadd = endAddress
                order.order_pretime = starttime
                order.order_passenger = passengerName
                order.order_tel = passengertel
                order.order_starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                order.order_distance = distance
                order.order_price = price
                order.order_state = 12
                order.order_type = ordertype
                order.save()
                jm.id = 1
                orderid = OrderInfo.objects.all().order_by("-order_id")[0].order_id
                jm.datas = orderid
            else:
                userInfo = json.loads(infos)
                order = OrderInfo()
                order.user_id = userInfo['user_id']
                order.order_startadd = startAddress
                order.order_destadd = endAddress
                order.order_pretime = starttime
                order.order_passenger = userInfo['user_nickname']
                order.order_tel = userInfo['user_tel']
                order.order_starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                order.order_distance = distance
                order.order_price = price
                order.order_state = 12
                order.order_type = ordertype
                order.save()
                jm.id = 1
                orderid = OrderInfo.objects.all().order_by("-order_id")[0].order_id
                jm.datas = orderid
    else:
        jm.id = -1
        jm.msg = '登录失效,请重新登录'
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def checkOrderstate(req):
    jm = jsonMsg()
    oid = req.GET.get('orderId')
    orderInfos = OrderInfo.objects.filter(order_id=oid)[0]
    if orderInfos.order_state == 13:
        jm.id = 1
        driverId = orderInfos.driver_id
        driverInfo = DriverInfo.objects.filter(driver_id=driverId)[0]
        jm.data1 = {
            'drname': driverInfo.driver_name,
            'drtel': driverInfo.driver_tel,
            'drplate': driverInfo.driver_plate,
            'carcolor': driverInfo.driver_carcolor,
            'cartbrand': driverInfo.driver_carbrand,
            'cartype': driverInfo.driver_cartype
        }
    else:
        jm.id = -1

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def cancelOrder(req):
    jm = jsonMsg()
    oid = req.GET.get('orderId')
    orderInfos = OrderInfo.objects.filter(order_id=oid)[0]
    orderInfos.order_state = 19
    orderInfos.save()
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def addPassenger(req):
    jm = jsonMsg()
    passengerName = req.GET.get('passengerName')
    passengerTel = req.GET.get('passengerTel')
    token = req.GET.get('token')
    user = redis_get(token)

    if user != None and user != '':
        uid = user['user_id']
        historypassenger = HistoryPassenge()
        historypassenger.user_id = uid
        historypassenger.historypassenge_name = passengerName
        historypassenger.historypassenge_tel = passengerTel
        historypassenger.save()
        jm.id = 1
    else:
        jm.id = -1
        jm.msg = '登录失效,请重新登录'

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def checkhistoryPassenger(req):
    jm = jsonMsg()
    token = req.GET.get('token')
    user = redis_get(token)
    if user != None and user != '':
        uid = user['user_id']
        infos = HistoryPassenge.objects.filter(user_id=uid).order_by("-historypassenge_id")[0:3]
        passengerList = []
        for i in range(len(infos)):
            j = model_to_dict(infos[i])
            passengerList.append(j)
        if infos != '' and infos != None:
            jm.id = 1
            jm.datas = passengerList
        else:
            jm.id = -1
    else:
        jm.id = -1
        jm.msg = '登录失效，请重新登录'
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def getOrderlist(req):
    jm = jsonMsg()
    current_page = req.GET.get('currentPage')
    per_page = req.GET.get('perPage')
    token = req.GET.get('token')
    user = redis_get(token)
    if user != None and user != '':
        uid = user['user_id']
        start = (int(current_page) - 1) * int(per_page)
        end = int(current_page) * int(per_page)
        # (Q(order_type=1)&(Q(order_state=19)|Q(order_state=17)|Q(order_state=18)))
        # (Q(order_type=3)&(Q(order_state=19)|Q(order_state=17)|Q(order_state=18)))
        # Q(order_type=3)
        orderlist = OrderInfo.objects.filter( Q(user_id=uid)  ).order_by('-order_starttime')[start:end]
        lists = []
        if len(orderlist) > 0:
            for i in range(len(orderlist)):
                j = model_to_dict(orderlist[i])
                j['order_starttime'] = str(j['order_starttime'].strftime("%Y-%m-%d %H:%M:%S"))
                j['order_desttime'] = str(j['order_desttime'])
                j['order_type'] = StateData.objects.filter(state_id=j['order_type'])[0].state_name
                j['order_state'] = StateData.objects.filter(state_id=j['order_state'])[0].state_name
                if(j['driver_id'] >0):
                    driverInfos = DriverInfo.objects.filter(driver_id=j['driver_id'])[0]
                    j['driver_id'] = model_to_dict(driverInfos)['driver_id']
                elif(j['driver_id'] ==0):
                    j['driver_id'] = 0
                lists.append(j)

        jm.datas = lists
        jm.id = len(OrderInfo.objects.filter(user_id=uid))
    else:
        jm.id = -1
        jm.msg = '登录失效'
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def callHitch(req):
    jm = jsonMsg()
    startAddress = req.GET.get('startAddress')
    destAddress = req.GET.get('destAddress')
    hitchTime = req.GET.get('hitchTime')
    ordertype = req.GET.get('ordertype')
    price = req.GET.get('price')
    distance = req.GET.get('distance')
    token = req.GET.get('token')
    re = redis.Redis(decode_responses=True)
    infos = re.get(token)
    if infos !=None and infos != "":
        userInfo = json.loads(infos)
        order = OrderInfo()
        order.user_id = userInfo['user_id']
        order.order_startadd = startAddress
        order.order_destadd = destAddress
        order.order_pretime = hitchTime
        order.order_passenger = userInfo['user_nickname']
        order.order_tel = userInfo['user_tel']
        order.order_starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order.order_distance = distance
        order.order_price = price
        order.order_state = 12
        order.order_type = ordertype
        order.save()
        jm.id = 1
        orderid = OrderInfo.objects.all().order_by("-order_id")[0].order_id
        jm.datas = orderid
    else:
        jm.id = -1
        jm.msg = "登录失效，请重新登录"
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def checkMoney(req):
     jm = jsonMsg()
     token = req.GET.get('token')
     re = redis.Redis(decode_responses=True)
     infos = re.get(token)
     if infos != None and infos != "":
         userInfo = json.loads(infos)
         jm.datas = userInfo['user_money']
         jm.id = 1
     else:
         jm.id = -1
         jm.msg = "登录失效，请重新登录"
     return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def addMoney(req):
    jm = jsonMsg()
    token = req.GET.get('token')
    money = req.GET.get('money')
    user = redis_get(token)
    re = redis.Redis(decode_responses=True)
    if user != None and user != "":
        money = int(money) + user['user_money']
        openid = user['user_mini_openid']
        infos = UserInfo.objects.filter(user_mini_openid=openid)[0]
        infos.user_registtime = str(infos.user_registtime)
        infos.user_money = money
        infos.save()
        re.set(token, json.dumps(model_to_dict(infos)), ex=7000)
        jm.id = 1
    else:
        jm.id = -1
        jm.msg = "登录失效，请重新登录"
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def overOrder(req):
    jm = jsonMsg()
    oid = req.GET.get('orderId')
    orderInfos = OrderInfo.objects.filter(order_id=oid)[0]
    if orderInfos.order_state == 15:
        jm.id = 1

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def paymoney(req):
    jm = jsonMsg()
    oid = req.GET.get('orderId')
    money = req.GET.get('money')
    money = float(money)
    token = req.GET.get('token')
    user = redis_get(token)
    re = redis.Redis(decode_responses=True)
    if user != None and user != "":
        if money < user['user_money']:
            openid = user['user_mini_openid']
            infos = UserInfo.objects.filter(user_mini_openid=openid)[0]
            infos.user_registtime = str(infos.user_registtime)
            infos.user_money = round((user['user_money'] - money),2)
            infos.save()
            re.set(token, json.dumps(model_to_dict(infos)), ex=7000)
            orderInfo = OrderInfo.objects.filter(order_id=oid)[0]
            orderInfo.order_state = 17
            orderInfo.order_starttime = str(orderInfo.order_starttime)
            orderInfo.order_desttime = str(orderInfo.order_desttime)
            orderInfo.save()
            jm.id = 1
            jm.msg = '支付成功'
        else:
            jm.id = 0
            jm.msg = "请去个人中心的我的钱包进行充值！"
    else:
        jm.id = -1
        jm.msg = "登录失效，请重新登录"
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def myorderPay(req):
    jm = jsonMsg()
    oid = req.GET.get('oid')
    money = req.GET.get('price')
    money = float(money)
    token = req.GET.get('token')
    user = redis_get(token)
    re = redis.Redis(decode_responses=True)
    if user != None and user != "":
        if money < user['user_money']:
            openid = user['user_mini_openid']
            infos = UserInfo.objects.filter(user_mini_openid=openid)[0]
            infos.user_registtime = str(infos.user_registtime)
            infos.user_money = round((user['user_money'] - money), 2)
            infos.save()
            re.set(token, json.dumps(model_to_dict(infos)), ex=7000)
            orderInfo = OrderInfo.objects.filter(order_id=oid)[0]
            orderInfo.order_state = 17
            orderInfo.save()
            jm.id = 1
            jm.msg = '支付成功'
        else:
            jm.id = 0
            jm.msg = "请去个人中心的我的钱包进行充值！"
    else:
        jm.id = -1
        jm.msg = "登录失效，请重新登录"
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")
#陈静
def getUserState(request):
    reqObj = json.loads(request.body)
    jm=jsonMsg()
    state_type = reqObj.get("state_type")
    StateDataArr=StateData.objects.filter(state_type=state_type)
    for i in range(len(StateDataArr)):
        a = model_to_dict(StateDataArr[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


# 用户数据
def User(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    state_id = reqObj.get("state_id")
    time1 = reqObj.get("time1")
    time2=reqObj.get("time2")
    input3 =reqObj.get("input3")
    start = reqObj.get("start")
    end = reqObj.get("end")
    print(start,end)
    UserArr = UserInfo.objects.all()

    if state_id is not None and state_id !="":
        UserArr = UserArr.filter(
            Q(user_state__icontains=state_id)
        )

    if input3 is not  None and input3 !="":
        UserArr = UserArr.filter(
            Q(user_nickname__icontains=input3)
        )

    if time1 is not  None and time1 !="":
        UserArr =  UserArr.filter(
            Q(user_registtime__gte=time1)
        )

    if time2 is not  None and time2 !="":
        dt = datetime.datetime.strptime(time2, "%Y-%m-%d")
        out_date = (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if out_date:
            UserArr = UserArr.filter(
                Q(user_registtime__lte=out_date)
            )

    jm.id = len(UserArr)
    UserArr = UserArr[start:end]

    for item in range(len(UserArr)):
        a = model_to_dict(UserArr[item])
        a['user_registtime'] = str(a['user_registtime'])
        a['user_registtime'] = a['user_registtime'][0:19]
        employee_state = a['user_state']
        state_name = StateData.objects.get(state_id=employee_state).state_name
        a['user_state_name'] = state_name
        jm.datas.append(a)
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")



# 用户订单详情
def userOrders(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    state_id = reqObj.get("state_id")
    user_id=reqObj.get('user_id')
    time1 = reqObj.get("time1")
    time2 = reqObj.get("time2")
    start = reqObj.get("start")
    end = reqObj.get("end")
    userOrderArr=OrderInfo.objects.filter(user_id=user_id)
    userOrderArr= userOrderArr.filter(
        Q(driver_id__gt=0)
    )
    if state_id is not None and state_id !="":
        userOrderArr= userOrderArr.filter(
            Q(order_state__icontains=state_id)
        )

    if time1 is not  None and time1 !="":
        userOrderArr=  userOrderArr.filter(
            Q(order_starttime__gte=time1)
        )
    if time2 is not  None and time2!="":
        dt = datetime.datetime.strptime(time2, "%Y-%m-%d")
        out_date = (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if out_date:
            userOrderArr= userOrderArr.filter(
                Q(order_desttime__lte=out_date)
            )
    jm.id = len(userOrderArr)
    userOrderArr =userOrderArr[start:end]
    for i in range(len(userOrderArr)):
        a = model_to_dict(userOrderArr[i])
        a['order_starttime'] = str(a['order_starttime'])
        a['order_starttime'] = a['order_starttime'][0:19]

        a['order_desttime'] = str(a['order_desttime'])
        a['order_desttime'] = a['order_desttime'][0:19]
        # 司机名称
        driver_id = a['driver_id']
        if driver_id>0:
            driver_name = DriverInfo.objects.get(driver_id=driver_id).driver_name
            a['driver_name'] = driver_name
            # 用户名称
            user_id = a['user_id']
            user_nickname = UserInfo.objects.get(user_id=user_id).user_nickname
            a['user_nickname'] = user_nickname
            # 订单状态
            order_state = a['order_state']
            state_name = StateData.objects.get(state_id=order_state).state_name
            a['state_name'] = state_name
            # 订单类型
            order_type = a['order_type']
            state_name = StateData.objects.get(state_id=order_type).state_name
            a['state_type'] = state_name
            jm.datas.append(a)
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def commitCom(req):
    jm = jsonMsg()
    oid = req.GET.get("orderId")
    suggest = req.GET.get("suggest")
    sorce = req.GET.get("sorce")
    comment = Comments()
    comment.order_id = int(oid)
    comment.comments_content = suggest
    comment.comments_level = float(sorce)
    comment.comments_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment.save()
    orderInfos = OrderInfo.objects.filter(order_id=oid)[0]
    orderInfos.order_state = 18
    orderInfos.save()
    jm.msg = '评价成功！欢迎下次继续打车！'

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")