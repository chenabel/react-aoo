import datetime
import json

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse


from company.models import EmployeeInfo, StateData, Role, Service, Province
from company.util.CommonUtils import md5String
from step4_django.dto.jsonMsg import jsonMsg


def getEmployeeInfo(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    state = reqObj.get("state")
    input3 = reqObj.get("input3")
    time1 = reqObj.get("time1")
    print(time1)
    # time1=str(time1)

    time2 = reqObj.get("time2")
    print(time2)
    end = reqObj.get("end")
    start = reqObj.get("start")
    employeeInfoArr=EmployeeInfo.objects.all()
    jm.msgnums = len(employeeInfoArr)
    employeeInfoArr1=EmployeeInfo.objects.filter()
    if state:
        employeeInfoArr = employeeInfoArr.filter(
            Q(employee_state__icontains=state)
        )
        jm.msgnums = len(employeeInfoArr)

    if time1:
        employeeInfoArr = employeeInfoArr.filter(
            Q(employee_registtime__gte=time1)
        )
        jm.msgnums = len(employeeInfoArr)
    if time2:
        dt = datetime.datetime.strptime(time2, "%Y-%m-%d")
        out_date = (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if out_date:
            employeeInfoArr = employeeInfoArr.filter(
                Q(employee_registtime__lte=out_date)
            )
            jm.msgnums = len(employeeInfoArr)

    if input3:
        employeeInfoArr = employeeInfoArr.filter(
            Q(employee_tel__icontains=input3)
        )
        jm.msgnums = len(employeeInfoArr)
    # print(employeeInfoArr)

    employeeInfoArr=employeeInfoArr[int(start):int(end)]
    for i in range(len(employeeInfoArr)):
        a=model_to_dict(employeeInfoArr[i])


        a['employee_registtime']=str(a['employee_registtime'])
        a['employee_registtime']=a['employee_registtime'][0:19]

        state=a['employee_state']
        state_name = StateData.objects.get(state_id=state).state_name
        a['state_name'] = state_name
        # a['employee_pwd']=md5String(a['employee_pwd'])
        # print(a['employee_pwd'])
        jm.datas.append(a)
        # print(a)

    # print(jm.datas)


    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def Stafflocking(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    employee_id = reqObj.get("employee_id")
    driver = EmployeeInfo.objects.get(employee_id=employee_id)
    driver.employee_state = 21
    driver.save()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def Staffunlock(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    employee_id = reqObj.get("employee_id")
    driver = EmployeeInfo.objects.get(employee_id=employee_id)
    driver.employee_state = 20
    driver.save()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def getstaffState(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    state_type = reqObj.get("staffState")
    StateDataArr = StateData.objects.filter(state_type=state_type)
    for i in range(len(StateDataArr)):
        a = model_to_dict(StateDataArr[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def Staffdelete(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    employee_id = reqObj.get("employee_id")
    EmployeeInfo.objects.filter(employee_id=employee_id).delete()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def emjurisdiction(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    role_id = reqObj.get("role_id")
    roleArr = Role.objects.filter(role_id=role_id)
    for i in range(len(roleArr)):
        a=model_to_dict(roleArr[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def getroles(request):
    jm = jsonMsg()
    roleArr = Role.objects.filter()
    for i in range(len(roleArr)):
        a = model_to_dict(roleArr[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def baocun(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    employee_id = reqObj.get("employee_id")
    # print(employee_id)
    role_id = reqObj.get("role_id")
    # print(role_id)
    EmployeeInfo.objects.filter(employee_id=employee_id).update(role_id=role_id)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def Addemployees(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    name = reqObj.get("name")
    pwd = reqObj.get("pwd")
    pwd = md5String(pwd)
    tel = reqObj.get("tel")
    # print(tel)
    role_id = reqObj.get("role_id")
    now = datetime.datetime.now()
    time=now.strftime("%Y-%m-%d %H:%M:%S")
    print(time,123)
    employeeInfo = EmployeeInfo(
        employee_name=name,
        employee_pwd=pwd,
        employee_tel=tel,
        employee_state=20,
        employee_registtime=time,
        role_id=role_id
    )
    employeeInfo.save()
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def staffsave(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    employeeIds = reqObj.get("employeeIds")
    names = reqObj.get("names")
    pwds = reqObj.get("pwds")
    tels = reqObj.get("tels")
    employeeInfo = EmployeeInfo.objects.get(employee_id=employeeIds)
    employeeInfo.employee_name = names
    employeeInfo.employee_pwd = pwds
    employeeInfo.employee_tel = tels
    employeeInfo.save()


    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def login(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    acc = reqObj.get("acc")
    pwd = reqObj.get("pwd")
    pwd = md5String(pwd)
    # employee_tel = acc, employee_pwd = pwd
    employeeInfo=EmployeeInfo.objects.filter()
    # print(employeeInfo['role_id'])
    for i in range(len(employeeInfo)):
        a=model_to_dict(employeeInfo[i])
        # print(a)
        if a['employee_tel'] == acc and a['employee_pwd'] == pwd and a['employee_state']==20:
            jm.msg = "登入成功"
            jm.id = a['role_id']
            break
        else:
            jm.msg = "登入失败"


    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def getRolexx(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    acc = reqObj.get("acc")
    print(acc,"acc")

    employeeInfo=EmployeeInfo.objects.filter()
    for i in range(len(employeeInfo)):
        a=model_to_dict(employeeInfo[i])
        print(a)
        id=a["role_id"]
        state = a['employee_state']
        state_name = StateData.objects.get(state_id=state).state_name
        a['state_name'] = state_name
        a["role_name"]=Role.objects.get(role_id=id).role_name
        if a['employee_tel']==acc:
            if a['role_name'] == "客服管理员":
                jm.id = 0
            else:
                jm.id = 1
            # print(a)
            jm.datas.append(a['employee_name'])
            print(jm.datas)


    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def Servebaocun(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    input1 = reqObj.get("input1")
    input2 = reqObj.get("input2")
    img = reqObj.get("img")
    value = reqObj.get("value")
    service=Service(
        service_site=input1,
        service_img=img,
        service_site_info=input2,
        province_id=value
    )
    service.save()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def getshen(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)

    province=Province.objects.filter()
    for i in range(len(province)):
        a=model_to_dict(province[i])
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def getServe(request):
    jm = jsonMsg()
    reqObj = json.loads(request.body)
    input3 = reqObj.get("input3")
    end = reqObj.get("end")
    start = reqObj.get("start")
    service=Service.objects.filter()
    jm.msgnums=len(service)

    if input3!="" and input3 is not None:
        service = service.filter(
            Q(service_site__icontains=input3)
        )
        jm.msgnums = len(service)

    service = service[int(start):int(end)]

    for i in range(len(service)):
        a=model_to_dict(service[i])

        provinceid=a['province_id']
        province_name = Province.objects.get(province_id=provinceid).province_name
        a['province_name']=province_name
        jm.msg=a['service_img']
        # print(jm.msg)
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

