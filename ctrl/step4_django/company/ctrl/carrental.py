import json
import os

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse

from company.models import CarRentalInfo
from step4_django.dto.jsonMsg import jsonMsg
from step4_django.settings import BASE_DIR


def getCarrent(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    CarrName = reqObj.get("CarrName")
    end = reqObj.get("end")
    start = reqObj.get("start")
    CarentalInforArr=CarRentalInfo.objects.filter()
    jm.msgnums = len(CarentalInforArr)
    CarentalInforArr1=CarRentalInfo.objects.filter()

    if CarrName:
        CarentalInforArr = CarentalInforArr.filter(
            Q(car_brand__contains=CarrName)
        )
        jm.msgnums = len(CarentalInforArr)

    CarentalInforArr=CarentalInforArr[int(start):int(end)]
    for i in range(len(CarentalInforArr)):
        a=model_to_dict(CarentalInforArr[i])

        jm.datas.append(a)
        jm.msgnums = len(CarentalInforArr)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")



def scCarrental(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    car_id = reqObj.get("car_id")
    CarRentalInfo.objects.filter(car_id=car_id).delete()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def baocunMod(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    car_id = reqObj.get("car_id")
    car_brand = reqObj.get("car_brand")
    car_type = reqObj.get("car_type")
    car_color = reqObj.get("car_color")
    car_inventory = reqObj.get("car_inventory")
    car_rent = reqObj.get("car_rent")
    carRentalInfo = CarRentalInfo.objects.get(car_id=car_id)
    carRentalInfo.car_brand=car_brand
    carRentalInfo.car_type=car_type
    carRentalInfo.car_color=car_color
    carRentalInfo.car_inventory=car_inventory
    carRentalInfo.car_rent=car_rent
    carRentalInfo.save()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")


def goodsImg(request):
    jm = jsonMsg()
    print("试试有没有运行这里")
    fileObj = request.FILES["file"]
    schid = request.POST.get("schid")
    input1 = request.POST.get("input1")
    # print(input1)

    # print(schid)
    # print(fileObj)
    # 拼接保存的路径         项目名/static /uploads/文件名
    filename = os.path.join(BASE_DIR, "static", "upload", fileObj.name)
    # print(filename)

    # 打开保存的文件
    file = open(filename, 'wb')
    # 把上传的文件，写入到保存的文件中
    for chunk in fileObj.chunks():
        file.write(chunk)
        # print(4,chunk)

    file.close()

    img = "/static/upload/" + fileObj.name
    # print(img,"img")
    jm.datas=img
    # print(jm.datas)
    # 修改

    # print(img)
    # request.session["img"] = img

    # print(request.session["goodsImg"],"request.session")

    # res={"status":True,"msg":"success"}
    return HttpResponse(json.dumps, content_type="application/json")

def AddCarrental(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    input1 = reqObj.get("input1")
    input2 = reqObj.get("input2")
    input3 = reqObj.get("input3")
    input4 = reqObj.get("input4")
    input5 = reqObj.get("input5")
    img = reqObj.get("img")

    # goodsImg = request.session.get("goodsImg")
    # print(goodsImg,"goodsImg")

    carRentalInfo=CarRentalInfo(
        car_brand=input1,
        car_color=input2,
        car_type=input3,
        car_rent=input4,
        car_inventory=input5,
        car_image=img
    )
    carRentalInfo.save()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")