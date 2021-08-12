import json

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse

from company.models import City, Province
from step4_django.dto.jsonMsg import jsonMsg


def getCharge(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    end = reqObj.get("end")
    start = reqObj.get("start")
    CityName = reqObj.get("CityName")

    cityArr=City.objects.filter()

    cityArr1=City.objects.filter()

    if CityName:
        cityArr = cityArr.filter(
            Q(city_name__icontains=CityName)|Q(city_spell__icontains=CityName)|Q(city_firstletter__icontains=CityName)

        )
        jm.msgnums = len(cityArr)
        cityArr=cityArr[int(start):int(end)]
        for i in range(len(cityArr)):
            a = model_to_dict(cityArr[i])
            province_id = a['province_id']
            province_name = Province.objects.get(province_id=province_id).province_name
            a['province_name'] = province_name

            jm.datas.append(a)
            # print(len(a))
    else:
        cityArr=cityArr[int(start):int(end)]
        for i in range(len(cityArr)):
            a = model_to_dict(cityArr[i])
            province_id = a['province_id']
            province_name = Province.objects.get(province_id=province_id).province_name
            a['province_name'] = province_name

            jm.datas.append(a)
            # print(len(a))
        jm.msgnums =len(cityArr1)

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")

def baocunPrice(request):
    reqObj = json.loads(request.body)
    jm = jsonMsg()
    city_id = reqObj.get("city_id")
    city_smallprice = reqObj.get("city_smallprice")
    city_bigprice = reqObj.get("city_bigprice")

    city = City.objects.get(city_id=city_id)
    city.city_smallprice = city_smallprice
    city.city_bigprice = city_bigprice

    city.save()

    return HttpResponse(json.dumps(jm.__dict__, ensure_ascii=False), content_type="application/json")
