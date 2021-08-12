import datetime
import json
from encodings import undefined

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse

from company.models import Role, Menu, EmployeeInfo
from company.util.CommonUtils import md5String
from step4_django.dto.jsonMsg import jsonMsg
from step4_django.util.tools import ajax_success


def getRole(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    input3 = reqObj.get("input3")
    roleArr = Role.objects.filter()
    jm.msgnums = len(roleArr)
    roleArr1 = Role.objects.filter()
    end = reqObj.get("end")
    start = reqObj.get("start")
    if input3!="" and input3 is not None:
        roleArr = roleArr.filter(
            Q(role_name__contains=input3)
        )
        jm.msgnums = len(roleArr)

    roleArr=roleArr[int(start):int(end)]
    for i in range(len(roleArr)):
        a = model_to_dict(roleArr[i])
        # print(a)
        jm.datas.append(a)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def addRole(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    input1 = reqObj.get("input1")
    input2 = reqObj.get("input2")
    role = Role(
        role_name = input1,
        role_describe=input2
    )
    role.save()
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def authority(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    role_id = reqObj.get("id")
    MenuArr=Menu.objects.filter(role_id=role_id)

    for i in range(len(MenuArr)):
        a=model_to_dict(MenuArr[i])
        # print(a)
        jm.datas.append(a['menu_name'])

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def Roledeletes(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    role_id = reqObj.get("id")
    print(role_id)
    # role = Role.objects.get(role_id=role_id)
    # employeeInfo=EmployeeInfo.objects.filter()
    employeeInfo=EmployeeInfo.objects.filter(role_id=role_id).exists()
    print(employeeInfo)
    if employeeInfo==True:
        jm.id = 1
    else:
        Role.objects.filter(role_id=role_id).delete()
    # for i in range(len(employeeInfo)):
    #     a=model_to_dict(employeeInfo[i])
    #     print(a['role_id'])
    #     if a['role_id'] == role_id:
    #         print(a['role_id'],123)
    #         jm.id=1
    #         break
    #     else:
    #         # Role.objects.filter(role_id=role_id).delete()
    #         pass

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def getRoleMenu(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    menuArr=Menu.objects.filter(role_id=1)
    for i in range(len(menuArr)):
        a=model_to_dict(menuArr[i])
        # print(a['menu_name'])
        jm.datas.append(a['menu_name'])

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def baocunMenu(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    role_id = reqObj.get("role_id")

    checkboxGroup = reqObj.get("checkboxGroup")
    # print(role_id)
    # print(checkboxGroup)
    role=Role.objects.get(role_id=role_id)
    print(role.role_name)
    if role.role_name=="超级管理员":
        jm.id=1
    else:
        jm.id=2
        Menu.objects.filter(role_id=role_id).delete()
        for i in range(len(checkboxGroup)):
            # print(checkboxGroup[i])
            menu=Menu.objects.filter(menu_name=checkboxGroup[i])
            menu=menu.values('menu_name','menu_url').distinct()
            # print(menu)
            for j in range(len(menu)):
                print(menu[j]['menu_url'])
                menu = Menu(
                    menu_name=checkboxGroup[i],
                    menu_url=menu[j]['menu_url'],
                    role_id=role_id
                )
                menu.save()


    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def baochundisplay(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    role_id = reqObj.get("role_id")
    roleNane = reqObj.get("roleNane")
    roleInfo = reqObj.get("roleInfo")
    role = Role.objects.get(role_id=role_id)
    print(role.role_name)
    if role.role_name == "超级管理员":
        jm.id = 1
    else:
        jm.id=2
        role.role_name = roleNane
        role.role_describe = roleInfo
        role.save()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def getRegisterRole(request):
    jm = jsonMsg()
    roleArr = Role.objects.filter()
    for i in range(len(roleArr)):
        a = model_to_dict(roleArr[i])
        jm.datas.append(a)
    print(jm.datas)
    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def zhuche(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    name = reqObj.get("name")
    pwd = reqObj.get("pwd")
    pwd = md5String(pwd)
    tel = reqObj.get("tel")
    role_id = reqObj.get("role_id")
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    # print(time, 123)
    employeeInfo = EmployeeInfo.objects.filter(employee_tel=tel).exists()
    if employeeInfo==True:
        jm.id=1
    else:
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