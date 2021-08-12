// app.js
const host='http://127.0.0.1:8000/'
App({
  host,
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)


   
  },
  globalData: {
    userInfo: null,
    pageToHeight:wx.getSystemInfoSync().statusBarHeight+30+7,
    paddingTopNum:wx.getSystemInfoSync().statusBarHeight+7
  }
})
