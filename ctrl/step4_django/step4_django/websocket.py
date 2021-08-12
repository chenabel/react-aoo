import json
import time

from step4_django.util.ChatDataUtil import ChatDataUtil

orderList=[]
async def websocket_application(scope, receive, send):
    global orderList
    while True:
        event = await receive()
        if event['type'] == 'websocket.connect':
            await send({'type': 'websocket.accept'})
        if event['type'] == 'websocket.disconnect':
            print(orderList)
            if len(ChatDataUtil.User)>0:
                for i in range(0, len(ChatDataUtil.User)):
                    ChatDataUtil.User[i]['select']='智能'
            break
        if event['type'] == 'websocket.receive':
            data=event['text']
            data=json.loads(data)
            #客服
            if 'chat' in data.keys():
                if data['serviceType'] == "newAdmin":
                    print("新增客服")
                    ChatDataUtil.Admin=send
                    ChatDataUtil.CurrUser=None
                    #用户列表
                    userAll=[]
                    if ChatDataUtil.User:
                        for i in range(0,len(ChatDataUtil.User)):
                            userAll.append(ChatDataUtil.User[i]['username'])
                    sendMsg={'serviceType':'initUserName','content':userAll}
                    await send({"type":"websocket.send","text":json.dumps(sendMsg,ensure_ascii=False)})
                if data['serviceType']=="newOnlineUser":
                    print("有新增用户")
                    #假设他是新用户
                    isNew=True
                    #判断是否在列表中存在，存在即不是新用户
                    if ChatDataUtil.User:
                        for i in range(0, len(ChatDataUtil.User)):
                            if ChatDataUtil.User[i]['username']==data['username']:
                                isNew=False
                                ChatDataUtil.User[i]['send']=send
                                historyChat=ChatDataUtil.User[i]['talk']
                    if isNew==False:
                        sendMsg = {'serviceType': 'historyChat', 'content': historyChat}
                        await send({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                    #若为新用户添加到用户列表中
                    if isNew==True:
                        dt = time.localtime()
                        ft = "%Y-%m-%d %H:%M:%S"
                        nt = time.strftime(ft, dt)

                        content = {'time': nt, 'who': '智能客服', 'msg': '您好！我是智能客服，有什么可以帮助您？', 'usertype': 'server'}
                        ChatDataUtil.User.append({"username": data['username'], "send": send, "talk": [content], "select": "智能"})
                        sendMsg = {'serviceType': 'sendToUserMsg', 'content': content}
                        await send({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                        #如果客服在线，告诉客服添加新用户
                        if ChatDataUtil.Admin:
                            sendMsg= {'serviceType': 'addNewUser', 'content': data['username']}
                            await ChatDataUtil.Admin({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                #用户发送消息
                if data['serviceType']=="userSendMsg":
                    print("客户在发送消息")
                    #找到这个用户的信息
                    userInfo=None
                    for i in range(0,len(ChatDataUtil.User)):
                        if ChatDataUtil.User[i]['username'] == data['from']:
                            userInfo= ChatDataUtil.User[i]
                    if data['msg']=="转人工客服":
                        if ChatDataUtil.Admin:
                            userInfo['select']="人工"
                            sendMsg={'serviceType': 'UserTip', 'content':"已转为人工客服"}
                            await send({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                        else:
                            sendMsg = {'serviceType': 'UserTip', 'content': "客服未在线，请稍候再转智人工客服"}
                            await send({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                    elif data['msg']=="转智能客服":
                        userInfo['select'] = "智能"
                        sendMsg = {'serviceType': 'UserTip', 'content': "已转为智能客服"}
                        await send({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                    else:
                        if userInfo['select']=="人工":
                            dt = time.localtime()
                            ft = "%Y-%m-%d %H:%M:%S"
                            nt = time.strftime(ft, dt)
                            content = {'time': nt, 'who': data['from'], 'msg': data['msg'],'usertype':'user'}
                            userInfo['talk'].append(content)
                            sendMsg={'serviceType': 'sendToUserMsg', 'content':content}
                            await send({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                            if ChatDataUtil.Admin and ChatDataUtil.CurrUser==data['from']:
                                await ChatDataUtil.Admin({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                            else:
                                sendMsg2 = {'serviceType': 'tip', 'content': data['from'] + "发送了一条新消息，请注意查收"}
                                await ChatDataUtil.Admin({"type": "websocket.send", "text": json.dumps(sendMsg2, ensure_ascii=False)})
                        else:
                            dt = time.localtime()
                            ft = "%Y-%m-%d %H:%M:%S"
                            nt = time.strftime(ft, dt)
                            #调用智能客服
                            AISay=None
                            if AISay == None:
                                AISay="目前还没有该问题的回答"
                            content1 = {'time': nt, 'who': data['from'], 'msg': data['msg'],'usertype':'user'}
                            content2={'time': nt, 'who': '智能客服', 'msg': AISay,'usertype':'server'}
                            userInfo['talk'].append(content1)
                            userInfo['talk'].append(content2)
                            sendMsg={'serviceType': 'sendToUserMsg','content': content1}
                            sendMsg2={'serviceType': 'sendToUserMsg', 'content': content2}
                            if ChatDataUtil.Admin and ChatDataUtil.CurrUser == data['from']:
                                await ChatDataUtil.Admin({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                                await ChatDataUtil.Admin({"type": "websocket.send", "text": json.dumps(sendMsg2, ensure_ascii=False)})
                            await send({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                            await send({"type": "websocket.send", "text": json.dumps(sendMsg2, ensure_ascii=False)})
                #客服发送信息
                if data['serviceType']=="serverSendMsg":
                    print("客服在发送消息")
                    userSend=None
                    dt = time.localtime()
                    ft = "%Y-%m-%d %H:%M:%S"
                    nt = time.strftime(ft, dt)
                    content = {'time': nt, 'who': data['from'], 'msg': data['msg'],'usertype':'server'}
                    if len(ChatDataUtil.User)>0:
                        for i in range(0,len(ChatDataUtil.User)):
                            if ChatDataUtil.User[i]['username']==data['touser']:
                                ChatDataUtil.User[i]['talk'].append(content)
                                userSend=ChatDataUtil.User[i]['send']

                    sendMsg= {'serviceType': 'sendToUserMsg', 'content': content}
                    await ChatDataUtil.Admin({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                    if userSend:
                        await userSend({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
                #改变当前用户
                if data['serviceType']=="changeUsr":
                    print("改变当前用户")
                    ChatDataUtil.CurrUser = data['user']
                    talk = None
                    for i in range(0,len(ChatDataUtil.User)):
                        if ChatDataUtil.User[i]['username'] == data['user']:
                            talk = ChatDataUtil.User[i]['talk']
                    sendMsg = {'serviceType': 'sendTalksInfo', 'content': talk}
                    await ChatDataUtil.Admin({"type": "websocket.send", "text": json.dumps(sendMsg, ensure_ascii=False)})
            #订单中实时通讯
            else:
                # 查找是否为新订单
                newOrder=True
                data['orderid']=int(data['orderid'])
                if len(orderList)>0:
                    for i in orderList:
                        if i['orderid']==data['orderid']:

                            if data['from']=='user':
                                i['user']=send
                            else:
                                i['driver']=send
                            newOrder=False
                            break
                    if newOrder==True:
                        order = {'orderid': data['orderid'], 'user': '', 'driver': '', 'talk': []}
                        if data['from'] == 'user':
                            order['user'] = send
                        else:
                            order['driver'] = send
                        orderList.append(order)
                else:
                    order = {'orderid': data['orderid'],'user':'','driver':'','talk':[]}
                    if data['from'] == 'user':
                        order['user'] = send
                    else:
                        order['driver'] = send
                    orderList.append(order)
                #发送消息
                if data['serviceType']=="sendMsg":
                    dt = time.localtime()
                    ft = "%Y-%m-%d %H:%M:%S"
                    nt = time.strftime(ft, dt)
                    for i in orderList:
                        if i['orderid']==data['orderid']:
                            content = {'time': nt, 'who': data['from'], 'msg': data['msg']}
                            if data['msg']!='':
                                i['talk'].append(content)
                            if i['user']!='':
                                userSend=i['user']
                                sendUserMsg = {'serviceType': 'sendToUserMsg','content': content}
                                await userSend({"type": "websocket.send", "text": json.dumps(sendUserMsg, ensure_ascii=False)})
                            if i['driver']!='':
                                driverSend=i['driver']
                                sendDriverMsg = {'serviceType': 'sendToDriverMsg','content':content}
                                await driverSend({"type": "websocket.send", "text": json.dumps(sendDriverMsg, ensure_ascii=False)})
                #发送定位
                if data['serviceType']=="sendLocation":
                    for i in orderList:
                        if i['orderid']==data['orderid']:
                            print('发送位置')
                            userSend = i['user']
                            if userSend!='':
                                sendUserMsg={'serviceType': 'sendLocation','content':data['msg'],'markers':data['markers']}
                                await userSend({"type": "websocket.send", "text": json.dumps(sendUserMsg, ensure_ascii=False)})
                if data['serviceType']=="alreadyGetPassenger":
                    for i in orderList:
                        if i['orderid']==data['orderid']:
                            userSend = i['user']
                            sendUserMsg = {'serviceType': 'alreadyGetPassenger', 'content': '已接到乘客'}
                            await userSend({"type": "websocket.send", "text": json.dumps(sendUserMsg, ensure_ascii=False)})

