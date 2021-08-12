// pages/myWallet/myWallet.js
const app = getApp()
Page({
  data: {
    headHeight: (wx.getSystemInfoSync().statusBarHeight + 7) * 2 + 70,
    money:0,
  },

  onShow () {
    wx.request({
      url:app.globalData.host + 'api/driver/getDriverMoney/',
      data:{
        did:wx.getStorageSync('openid')
      },
      method:'post',
      success:res=>{
        console.log(res)
        this.setData({
          money:res.data.money
        })
      }
    })
  },
  getMoneyClick(){
    wx.showToast({
      title: '该功能还未开放！',
      icon:"none"
    })
  }
})