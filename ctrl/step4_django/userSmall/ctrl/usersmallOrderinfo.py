import datetime
import json

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse

from company.models import StateData, Service
from driverSmall.models import DriverInfo
from step4_django.dto.jsonMsg import jsonMsg
from userSmall.models import OrderInfo, UserInfo


def getOrder(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    state_id = reqObj.get("state_id")
    end = reqObj.get("end")
    start = reqObj.get("start")
    time1 = reqObj.get("time1")
    time2 = reqObj.get("time2")
    orderInfoArr=OrderInfo.objects.filter()
    jm.msgnums = len(orderInfoArr)
    orderInfoArr = orderInfoArr.filter(
        Q(driver_id__gt=0)
    )
    if state_id:
        orderInfoArr = orderInfoArr.filter(
            Q(order_state__icontains=state_id)
        )
        jm.msgnums = len(orderInfoArr)
    if time1:
        orderInfoArr = orderInfoArr.filter(
            Q(order_starttime__gte=time1)
        )
        jm.msgnums = len(orderInfoArr)
    if time2:
        dt = datetime.datetime.strptime(time2, "%Y-%m-%d")
        out_date = (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if out_date:
            orderInfoArr = orderInfoArr.filter(
                Q(order_desttime__lte=out_date)
            )
            jm.msgnums = len(orderInfoArr)
    orderInfoArr=orderInfoArr[int(start):int(end)]
    for i in range(len(orderInfoArr)):
        a = model_to_dict(orderInfoArr[i])

        a['order_starttime'] = str(a['order_starttime'])
        a['order_starttime'] = a['order_starttime'][0:19]

        a['order_desttime'] = str(a['order_desttime'])
        a['order_desttime'] = a['order_desttime'][0:19]



        userid=a['user_id']
        user_name = UserInfo.objects.get(user_id=userid).user_nickname
        a['user_name']=user_name

        driverid=a['driver_id']
        driver_name=DriverInfo.objects.get(driver_id=driverid).driver_name
        a['driver_name']=driver_name

        state = a['order_state']
        state_name = StateData.objects.get(state_id=state).state_name
        a['state_name'] = state_name

        type = a['order_type']
        type_name = StateData.objects.get(state_id=type).state_name
        a['type_name'] = type_name


        jm.datas.append(a)


    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def getOrderState(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    orderState = reqObj.get("orderState")
    StateDataArr = StateData.objects.filter(state_type=orderState)
    for i in range(len(StateDataArr)):
        a = model_to_dict(StateDataArr[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def getorderdetails(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    orderdetails = reqObj.get("orderdetails")

    orderInfoArr = OrderInfo.objects.filter(order_id=orderdetails)

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

def getUserNum(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)

    userInfo=UserInfo.objects.filter(user_sex="男")

    nanNum=len(userInfo)
    print(nanNum,"男")
    jm.msgnums=nanNum
    userInfo = UserInfo.objects.filter(user_sex="女")

    nvNum = len(userInfo)
    print(nvNum, "女")
    jm.id = nvNum
    userInfo = UserInfo.objects.filter()
    cont=len(userInfo)
    jm.count=cont

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def getTurnNum(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    today = datetime.date.today()
    # print(today)
    orderInfo=OrderInfo.objects.filter(order_desttime__icontains=today)

    price1=0
    for i in range(len(orderInfo)):
        a=model_to_dict(orderInfo[i])
        print(a['order_price'])
        price1=price1+a['order_price']
    jm.price1=price1
    # print(jm.price1)

    qian=(today + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d")
    orderInfo1 = OrderInfo.objects.filter(order_desttime__icontains=qian)
    price2 = 0
    for i in range(len(orderInfo1)):
        a = model_to_dict(orderInfo1[i])
        # print(a)
        price2 = price2 + a['order_price']
    jm.price2= price2
    # print(jm.price2)

    this_week_start = today - datetime.timedelta(days=today.weekday())
    this_week_end = today + datetime.timedelta(days=6 - today.weekday())

    orderInfo2 = OrderInfo.objects.filter(Q(order_starttime__gte=this_week_start) & Q(order_desttime__lte=this_week_end))
    price3= 0
    for i in range(len(orderInfo2)):
        a=model_to_dict(orderInfo2[i])
        # print(a)
        price3=price3+ a['order_price']
    jm.price3=price3

    this_month_start = datetime.datetime(today.year, today.month, 1)
    this_month_end = datetime.datetime(today.year, today.month + 1, 1) - datetime.timedelta(days=1)
    orderInfo3 = OrderInfo.objects.filter(
        Q(order_starttime__gte=this_month_start) & Q(order_desttime__lte=this_month_end))
    price4 = 0
    for i in range(len(orderInfo3)):
        a = model_to_dict(orderInfo3[i])
        # print(a)
        price4 = price4 + a['order_price']
    jm.price4 = price4


    
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def getDistance(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    orderInfo = OrderInfo.objects.filter(order_distance__lt=5)
    jm.orderNum1=len(orderInfo)

    orderInfo1 = OrderInfo.objects.filter(Q(order_distance__gte=5) & Q(order_distance__lt=10))
    jm.orderNum2 = len(orderInfo1)

    orderInfo2 = OrderInfo.objects.filter(order_distance__gte=10)
    jm.orderNum3 = len(orderInfo2)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def dels(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    id = reqObj.get("id")
    Service.objects.filter(service_id=id).delete()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def baocunxx(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    input11 = reqObj.get("input11")
    input22 = reqObj.get("input22")
    value = reqObj.get("value")
    id = reqObj.get("id")

    service = Service.objects.get(service_id=id)
    service.service_site=input11
    service.service_site_info=input22
    service.province_id=value
    service.save()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")