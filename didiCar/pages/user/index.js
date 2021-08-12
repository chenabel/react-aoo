// pages/user/index.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    pageToHeight:app.globalData.pageToHeight,
    userInfo:{},
    tel:''
  },
  onLoad(){
     this.data.userInfo = wx.getStorageSync('userInfo')
     this.setData({
      userInfo:this.data.userInfo,
      tel:wx.getStorageSync('usertel')
     })
    
    
  },
  intoIndex(){
    wx.redirectTo({
      url: '../index/index',
    })
  },
  intoMyorder(){
    wx.redirectTo({
      url: '../myOrder/myOrder',
    })
  },
  intoMywallet(){
    wx.redirectTo({
      url: '../myWallet/myWallet',
    })
  }
  
})