import json

from django.http import HttpResponse

from company.models import News
from step4_django.dto.jsonMsg import jsonMsg


def findAllNews(res):
    js = jsonMsg()
    NewsArr = News.objects.filter(news_lang='zh')[:6]
    NewsArr1 = News.objects.filter(news_lang='en')[:6]
    for i in NewsArr:
        content={'id':i.id,'news_id':i.news_id,'news_title':i.news_title}
        js.datas.append(content)
    for i in NewsArr1:
        content={'id':i.id,'news_id':i.news_id,'news_title':i.news_title}
        js.data2.append(content)


    return HttpResponse(json.dumps(js.__dict__, ensure_ascii=False), content_type="application/json")

def FindNews(res):
    js = jsonMsg()
    data = json.loads(res.body)
    limit=data.get('limit')
    start=data.get('start')
    end=start+limit

    NewsArr = News.objects.filter(news_lang='zh')[start:end]
    NewsArr1 = News.objects.filter(news_lang='en')[start:end]

    for i in NewsArr:
        content={'id':i.id,'news_id':i.news_id,'news_title':i.news_title,'news_img':i.news_img}
        js.datas.append(content)
        # print(content
    print(js.datas)
    for i in NewsArr1:
        content={'id':i.id,'news_id':i.news_id,'news_title':i.news_title,'news_img':i.news_img}
        js.data2.append(content)

    count=News.objects.count()
    js.id=count

    return HttpResponse(json.dumps(js.__dict__, ensure_ascii=False), content_type="application/json")

def initNews(res):
    js = jsonMsg()
    data = json.loads(res.body)
    if 'id' in data.keys():
        print('有数据')
    else:
        print('没数据')
    id=data.get('id')
    NewsArr = News.objects.filter(news_lang='zh',news_id=id)
    NewsArr1 = News.objects.filter(news_lang='en',news_id=id)

    for i in NewsArr:
        content = {'id': i.id, 'news_id': i.news_id, 'news_title': i.news_title,'news_content': i.news_content, 'news_img': i.news_img}
        js.datas.append(content)
        i.news_time = str(i.news_time)
    for i in NewsArr1:
        content = {'id': i.id, 'news_id': i.news_id, 'news_title': i.news_title,'news_content': i.news_content,'news_img': i.news_img}
        js.data2.append(content)
        i.news_time = str(i.news_time)
    return HttpResponse(json.dumps(js.__dict__, ensure_ascii=False ,), content_type="application/json")
    # 以 json 格式的 字符串 传回前端
    # 传后端用 post 带上数据
