const app = getApp()

Page({
  data: {
    headHeight: (wx.getSystemInfoSync().statusBarHeight + 7) * 2 + 70,
    nowPageUrl:"",//给pageTab组件用
    orderLen:0,//今天接了几单
    driverMoney:0, //今日流水
    totalMileage:0, //总里程
    servicePoints:0,//服务分
    driverState:false,
    tipText:"休息中",
  },

  onLoad(){
    var url =getCurrentPages()[getCurrentPages().length-1].route
    console.log('当前页',url)
    this.setData({
      nowPageUrl:url,
      driverState:app.globalData.driverState
    })
    this.initPage()
  },

  onShow(){
    if(app.globalData.driverState2 == true){
      this.setData({
        driverState:false
      })
      this.changeState()
    }
  },

  initPage(){
    wx.request({
      url: app.globalData.host + 'api/driver/getDriverOrder/',
      data:{
        did:wx.getStorageSync('openid')
      },
      method:'post',
      success:res=>{
        console.log(res)
        this.setData({
          orderLen:res.data.orderLen, //今日接单
          driverMoney:res.data.money,
          totalMileage:res.data.totalMileage,
          servicePoints:res.data.servicePoints
        })
      }
    })
  },

  changeState(e){
    var that = this
    var animation  = wx.createAnimation({
      duration:500,
      timingFunction:'ease'
    })
    that.animation = animation
    if(that.data.driverState == false){
      animation.translateX(-175).step()
      this.setData({
        animationData: animation.export(),
        chooseSize:true,
        driverState:true,
        tipText:"工作中"
      })
      app.globalData.driverState2 = true
    }else{
      animation.translateX(0).step()
      this.setData({
        animationData: animation.export(),
        chooseSize:true,
        driverState:false,
        tipText:"休息中"
      })
      app.globalData.driverState2 = false
    }
    console.log(123) 
  },

  orderClick(){
    wx.redirectTo({
      url: '/pages/myOrderPage/myOrderPage',
    })
  },
  
  myWalletClick(){
    wx.redirectTo({
      url: '/pages/myWallet/myWallet',
    })
  },

  goOrderPage(){
    wx.redirectTo({
      url: '/pages/shunFeng/shunFeng',
    })
  },

  rulesClick(){
    wx.redirectTo({
      url: '/pages/rules/rules',
    })
  }

})

