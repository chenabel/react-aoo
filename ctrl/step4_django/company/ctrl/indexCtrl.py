import json

from django.forms import model_to_dict
from django.http import HttpResponse

from company.models import Province, City
from step4_django.dto.jsonMsg import jsonMsg


def selectProvince(res):
    js = jsonMsg()
    ProvinceArr=Province.objects.filter()
    for i in ProvinceArr:
        content={'province_id':i.province_id,'province_name':i.province_name}
        js.datas.append(content)


    return HttpResponse(json.dumps(js.__dict__, ensure_ascii=False), content_type="application/json")


def selectCity(res):
    js = jsonMsg()

    id= 0
    if 'id' in res.GET.keys():
        id = res.GET.get('id')


        province_id = id
        print(province_id,"province_id")
        cityArr=City.objects.filter(province_id=province_id)
        for i in cityArr:
            content={'city_id':i.city_id,'city_name':i.city_name,'city_smallprice':i.city_smallprice,'city_bigprice':i.city_bigprice,'province_id':i.province_id}
            print(content)
            js.data2.append(content)

    return HttpResponse(json.dumps(js.__dict__, ensure_ascii=False), content_type="application/json")

