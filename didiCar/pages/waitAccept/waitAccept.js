// pages/waitAccept/waitAccept.js
const app = getApp()
var webSocket=false
Page({

  /**
   * 页面的初始数据
   */
  data: {
      pageToHeight:app.globalData.pageToHeight,
      paddingTopNum:app.globalData.paddingTopNum,
      polyline: '',
      longitude: '',
      latitude: '',
      driverInfos:'',
      driverName:'',
      chat:false,
      allInfos:true,
      chatcontent:"",
      chatList:[],
      userhead:wx.getStorageSync('userInfo').avatarUrl,
      username:'乘客'+wx.getStorageSync('userInfo').nickName,
      top:'',
      run:true,
      wait:true,
      ing:false,
      over:false,
  },
  changeMessage(e){
    this.data.chatcontent = e.detail.value
  },
  sendMessage(e){
    const text={
      msg:this.data.chatcontent,
      orderid:wx.getStorageSync('orderId'),
      serviceType:'sendMsg',
      from:'user',
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
  chat(){
    this.setData({
      chat:true,
      allInfos:false
    })
  },
  closeChat1(){
    this.setData({
      chat:false,
      allInfos:true
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
      this.setData({
        polyline:wx.getStorageSync('polyline'),
        longitude:wx.getStorageSync('longitude'),
        latitude: wx.getStorageSync('latitude'),
        driverInfos:wx.getStorageSync('driverInfos'),
      })
  },
  pause(){
    this.data.run=false
  },
  continue(){
    this.data.run=true
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
      this.setData({
        driverName:this.data.driverInfos.drname.substr(0,1)+"师傅"
      })
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
            _this.sendMessage()
            wx.onSocketMessage(function(resp){
              let data=JSON.parse(resp.data)
              if(data.serviceType==='sendToUserMsg'){
                if(data.content.msg!==''){
                  _this.data.chatList.push(data.content)
                  _this.data.top=_this.data.chatList.length*1000
                }
                _this.setData({
                  chatList:_this.data.chatList,
                })
                if(_this.data.run){
                  _this.setData({
                    top: _this.data.top
                  })
                }
              }
              if(data.serviceType==='sendLocation'){
                data.markers.iconPath='/icons/car.png'
                _this.setData({
                  polyline:data.content,
                  markers:[data.markers]
                })
              }
              if(data.serviceType==='alreadyGetPassenger'){
                _this.setData({
                  wait:false,
                  ing:true
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
  },
  calltel(){
    wx.showModal({
      title: this.data.driverName+'手机号码',
      content: this.data.driverInfos.drtel,
    })
  },

})