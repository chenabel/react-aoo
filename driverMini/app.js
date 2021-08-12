
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
  },
  globalData: {
    userInfo: null,
    host:"http://127.0.0.1:8000/",
    cityName:"",
    driverTel:"13665093859",
    orderId:"63",
    tel:"",
    appid:"wx75e53db15a0e1dd6",
    secret:"94fdafabc42c562e2ac9d92ec5882f7a",
    jindu1:"", 
    weidu1:"",
    driverState:false, //判断司机状态
    driverState2:false, //判断司机状态
    isDisconnection:false,
  }
})
