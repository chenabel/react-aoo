// pages/waitAccept/waitAccept.js
const app = getApp()
var webSocket=false;
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
      money:'',
      pay:false,
      driverallInfos:true,
      comment:false,
      key: 0,//评分
      score:0.0,
      ordering:true,
      markers:''
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
        money:wx.getStorageSync('money')
      });
      this.overOrder();
  },
  onReady:function(options){
    const _this=this;
      wx.connectSocket({
        url: 'ws://127.0.0.1:8000/',
        header:{
          'content-type':'application/json'
        },
        success:function(res){
          console.log("客户端连接成功")
          wx.onSocketOpen(function(){
            console.log('webSocket已打开!')
            webSocket=true
            const text={
              msg:'',
              orderid:wx.getStorageSync('orderId'),
              serviceType:'sendMsg',
              from:'user',
            }
            if(webSocket){
              wx.sendSocketMessage({
                data:JSON.stringify(text),
              })
            }
            wx.onSocketMessage(function(resp){
              let data=JSON.parse(resp.data)
              console.log(data)
              if(data.serviceType==='sendLocation'){
                data.markers.iconPath='/icons/car.png'
                _this.setData({
                  polyline:data.content,
                  markers:[data.markers]
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
  comment(e){
    // console.log(e.detail.params);
    this.setData({
      score:e.detail.params
    })
  },
 
  overOrder(){
    this.countTimer=setInterval(() => {
      wx.request({
        url: app.host+'api/overOrder/?token='+wx.getStorageSync('token'),
        data:{
          orderId:wx.getStorageSync('orderId')
        },
        success:res=>{
          if(res.data.id==1){
            this.setData({
              pay:true,
              driverallInfos:false,
              ordering:false
            })
            clearInterval(this.countTimer)
          }
        }
      })
    }, 1000);
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
      this.setData({
        driverName:this.data.driverInfos.drname.substr(0,1)+"师傅"
      })
  },

  calltel(){
    wx.showModal({
      title: this.data.driverName+'手机号码',
      content: this.data.driverInfos.drtel,
    })
  },
  paymoney(){
    wx.request({
      url: app.host+'api/paymoney/?token='+wx.getStorageSync('token'),
      data:{
        money:this.data.money,
        orderId:wx.getStorageSync('orderId')
      },
      success:res=>{
        if(res.data.id==1){
           wx.showToast({
             title: res.data.msg,
             icon:"none"
           })
           this.setData({
            pay:false,
            comment:true,
           })
        }
        if(res.data.id == 0){
          wx.showToast({
            title: res.data.msg,
            icon:"none"
          })
          setTimeout(() => {
            wx.redirectTo({
              url: '../myWallet/myWallet',
            })
          }, 1000);
        }
        
      }
    })
  }
})