// pages/orderHall/orderHall.js
const app = getApp()
// const backgroundAudioManager = wx.getBackgroundAudioManager()
// backgroundAudioManager.title = '此时此刻'
// backgroundAudioManager.epname = '此时此刻'
// backgroundAudioManager.singer = '许巍'
// backgroundAudioManager.coverImgUrl = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000'
// // 设置了 src 之后会自动播放
// backgroundAudioManager.src = "http://audio04.dmhmusic.com/71_53_T10053603750_128_4_4_0_sdk-cpm/cn/0103/M00/10/C0/ChR45V8hec-AV2l2AAdYWk2-OrY737.mp3?xcode=90e8f61412fd16e781aca8eb499fb22d43b03cb"
// backgroundAudioManager.play()

Page({
  data: {
    headHeight: (wx.getSystemInfoSync().statusBarHeight + 7) * 2 + 70,
    orderList: [{
      order_price: 987, // 订单价格
      order_startadd: '福州市仓山区大榕树文化创意园', // 出发地 
      order_destadd: '上海浦东区黄埔东路古道街3号楼', // 目的地
      order_starttime: '14:42',
      order_distance: '4.5km',
      order_id: "1123"
    }],
    openid: '',// 司机openid
    isOrderList: true,
    nowPageUrl: "",
    timer:''
  },

  onLoad() {
    var that = this
    this.getNowUrl()
    wx.request({
      url: app.globalData.host + 'api/driver/allOrder/',
      method: 'post',
      data: {
        type: "rightNow",
        state: 1
      },
      success(res) {
        console.log(res.data.allOrder)
        if (res.data.allOrder.length == 0) {
          that.setData({
            isOrderList: false
          })
          return
        }
        that.setData({
          orderList: res.data.allOrder
        })
      }
    })
  },

  onShow() {
    var that = this
    var openid = wx.getStorageSync('openid')
    let e = this;
		//执行定时器任务
    that.setData({
      openid: openid,
      timer:setInterval(function () {
        that.getAllOrder();
      }, 3000)
    })
    wx.request({
      url: app.globalData.host + 'api/driver/isDriverOrder/',
      data: {
        getOrder: true,
        openid: openid
      },
      method: 'post',
      success: res => {
        console.log(res)
        if (res.data.flage != false) {
          app.globalData.orderId = res.data.order.order_id
          app.globalData.isDisconnection = true
          wx.redirectTo({
            url: '/pages/orderPage/orderPage',
          })
        }
      }
    })
  },

  getNowUrl() {
    var url = getCurrentPages()[getCurrentPages().length - 1].route
    console.log('当前页', url)
    this.setData({
      nowPageUrl: url
    })
  },

  //??????
  getOrder(e) {
    if (app.globalData.driverState2 != true) {
      wx.showToast({
        title: "您还在休息中哦！",
        icon: "loading"
      })
      return
    }
    var that = this
    var oid = e.currentTarget.dataset.orderid
    wx.request({
      url: app.globalData.host + 'api/driver/getorder/',
      method: 'post',
      data: {
        openid: this.data.openid,
        oid: oid,
        driverTel: app.globalData.driverTel
      },
      success(res) {
        if(res.data.type == 'success'){
          app.globalData.orderId = e.currentTarget.dataset.orderid
          console.log('kkk', res)
          wx.redirectTo({
            url: "/pages/takeUser/takeUser",
          })
        }else if (res.data.type == 'error'){
          wx.showToast({
            title: res.data.msg,
            icon:res.data.type
          })
          that.getAllOrder()
        }
      }
    })
  },

  onReady(e) {
    // 使用 wx.createAudioContext 获取 audio 上下文 context
    this.audioCtx = wx.createAudioContext('myAudio')
  },
  
  getAllOrder(){
    var that = this
    wx.request({
      url: app.globalData.host + 'api/driver/allOrder/',
      method: 'post',
      data: {
        type: "rightNow",
        state: 1
      },
      success(res) {
        console.log(res)
        if (res.data.allOrder.length == 0) {
          that.setData({
            isOrderList: false
          })
          return
        }
        that.setData({
          isOrderList:true,
          orderList: res.data.allOrder
        })
      }
    })
  },

  _onPulling(e){
    this.getAllOrder()
    console.log("onPulling")
  },

  _onRefresh(e) {
    console.log('_onRefresh')
  },

  _onRestore(e) {
    console.log('_onRestore')
  },

  _onAbort(e) {
    console.log('_onAbort')
  },

  _onRefreshEnd() {
    console.log('_onRefreshEnd')
  },

  _onLoadmore(e) {
    console.log('_onLoadmore')
  },
  
  onUnload:function(){ 
		var that = this;
    clearInterval(that.data.timer);
    this.setData({
			timer: null
		})
  },
})