// pages/loginPage/login.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
        pageToHeight:app.globalData.pageToHeight,
        paddingTopNum:app.globalData.paddingTopNum,
        // 用户信息获取
        userInfo: {},
  },

  
   // 获取用户信息
   getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认
    // 开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '用于完善会员资料', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        this.setData({
          userInfo: res.userInfo,
        }),
        wx.login({
          success:res=>{
            let code = res.code;
            wx.request({
              url: app.host+ 'api/userLogin/?code='+code,
              data:{
                userInfo:this.data.userInfo
              },
              success:res=>{
                wx.setStorageSync('token', res.data.datas.token);
                
                if(res.data.id==1){
                  wx.redirectTo({
                    url: '../phonePage/phone'
                  })
                }else{
                  wx.setStorageSync('usertel', res.data.data2)
                  wx.redirectTo({
                    url: '../index/index',
                  })
                }
              }
            })
          }
        })
        console.log(res.userInfo);
        // 用户信息存入storage
        wx.setStorageSync('userInfo', this.data.userInfo);
        
      }
    })
  },

  intoIndex(){
    wx.redirectTo({
      url: '../index/index',
    })
  },



})