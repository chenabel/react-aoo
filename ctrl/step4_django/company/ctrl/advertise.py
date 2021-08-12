
import json
import datetime
import time

from django.forms import model_to_dict
from django.http import HttpResponse
from lxml.html.builder import Q


from company.models import *
from step4_django.dto.jsonMsg import jsonMsg





def getAdvertiseInfo(request):
    reqObj = json.loads(request.body)
    start = reqObj.get("start")
    end = reqObj.get("end")
    advertiseArr=Advertise.objects.all()
    advertiseArr1 = Advertise.objects.filter()
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    jm=jsonMsg()

    advertiseArr = advertiseArr[start:end]
    for i in range(len(advertiseArr)):
        a = model_to_dict(advertiseArr[i])
        a['advertise_starttime'] = str(a['advertise_starttime'])
        a['advertise_starttime'] = a['advertise_starttime'][0:19]

        a['advertise_desttime'] = str(a['advertise_desttime'])
        a['advertise_desttime'] = a['advertise_desttime'][0:19]

        advertise_state = a['advertise_state']
        state_name = StateData.objects.get(state_id=advertise_state).state_name
        a['advertise_state_name'] = state_name

        if a['advertise_desttime']<NowTime:
            advertise_id = a['advertise_id']
            Advertise.objects.filter(advertise_id=advertise_id).update(advertise_state=23)
        jm.datas.append(a)
        jm.id=len(advertiseArr1)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def  deleteAdvertise(request):
    reqObj = json.loads(request.body)
    advertise_id=reqObj.get('advertise_id')
    jm = jsonMsg()

    advertiseArr = Advertise.objects.filter(advertise_id=advertise_id).delete()
    jm.msg='删除成功'
    jm.id=1


    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def addAdvertise(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    input1 = reqObj.get("input1")
    time1 = reqObj.get("time1")

    time2 = reqObj.get("time2")



    newAdvertise = Advertise(
        advertise_image =input1,
        advertise_url=input1,
        advertise_starttime=time1,
        advertise_desttime=time2,
        advertise_state=22,
    )
    newAdvertise.save()
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")