// pages/user/chat.js
const app=getApp()
var webSocket=false
Page({
  data: {
    pageToHeight:app.globalData.pageToHeight,
    paddingTopNum:app.globalData.paddingTopNum,
    chatcontent:"",
    chatArr:[],
    user
  },
  changeMessage(e){
    this.data.chatcontent=e.detail.value
  },
  newUser(){
    const text={
      chat:'',
      username:wx.getStorageSync('userInfo').nickName,
      serviceType:'newOnlineUser',
    }
    if(webSocket){
      wx.sendSocketMessage({
        data: JSON.stringify(text),
      })
      console.log('添加新用户')
    }
  },
  sendMessage(e){
    const text={
      chat:'',
      msg:this.data.chatcontent,
      serviceType:'userSendMsg',
      from:wx.getStorageSync('userInfo').nickName,
    }
    if(webSocket){
      wx.sendSocketMessage({
        data: JSON.stringify(text),
      })
      this.setData({
        chatcontent:''
      })
    }
  },
  onLoad(options){
    const _this=this;
    wx.connectSocket({
      url: 'ws://127.0.0.1:8000/',
      header:{
        'content-type':'application/json'
      },
      success:function(res){
        console.log("客户端连接成功")
        wx.onSocketOpen(function(){
          console.log('webSocket已打开！')
          webSocket=true
          _this.newUser()
          wx.onSocketMessage(function(resp){
            const data=JSON.parse(resp.data)
            if(data.serviceType==='sendToUserMsg'){
              _this.data.chatArr.push(data.content)
              console.log(_this.data.chatArr)
              _this.setData({
                chatArr:_this.data.chatArr
              })
            }
            if(data.serviceType==='UserTip'){
              wx.showToast({
                title: data.content,
                icon:'none',
                duration:1000
              })
            }
            if(data.serviceType==='historyChat'){
              _this.data.chatArr=data.content
              _this.setData({
                chatArr:_this.data.chatArr
              })
            }
          })
          wx.onSocketClose(function(){
            console.log('webSocket已关闭！');
          })
        })
      },
      complete:function(err){
        console.log(err)
      }
    })
  }
})