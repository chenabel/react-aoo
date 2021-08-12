// pages/phonePage/phone.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    pageToHeight:app.globalData.pageToHeight,
    paddingTopNum:app.globalData.paddingTopNum,
    phoneNum:'', //手机号码
    codeNum:'',  // 验证码
    downCount:0, //倒计时
  },

    // 获取手机号码
    inputPhone(e){
      this.setData({
        phoneNum:e.detail.value
      })
    },
    
    // 发送验证码
  sendCode(e){
    // 判断手机号码是否输入正确
    if(!/^1[3456789]\d{9}$/.test(this.data.phoneNum)){
      wx.showToast({
        title: '手机号码输入有误！',
        icon:'none',
        duration:2000,
      })
      return;
    }
    // 输入了正确的手机号码后
    wx.request({
      url: app.host+ 'api/userSendCode/',
      data:{
        phoneNum:this.data.phoneNum
      },
      success:res=>{
          console.log(res);
          if(res.data.id == 1){
            this._downCount(60)
            return;
          }
          wx.showToast({
            title: '',
            icon:'none'
          })
      }
    })
  },
  // 倒计时
  _downCount(time){
    this.setData({
      downCount:time
    })
    time--;
    if(time < 0){
      return
    }
    // 所有的匿名函数几乎都可以用箭头函数
    // 不需要this指向的地方
    setTimeout(v => {
      // 递归
      this._downCount(time)
    }, 1000);
  },

  // 获取输入验证码
  inputCode(e){
    this.setData({
      codeNum:e.detail.value
    })
  },

  // 验证码确认
  verify(){
    const token = wx.getStorageSync('token')
    wx.request({
      url: app.host+'api/userVerify/?token='+token,
      data:{
        phoneNum:this.data.phoneNum,
        codeNum:this.data.codeNum,
      },
      success:res=>{
        console.log(res)
        if(res.data.id ==1){
          wx.setStorageSync('usertel', res.data.datas.tel)
          wx.showToast({
            title: res.data.msg,
            icon:'none'
          })
          wx.redirectTo({
            url: '../index/index',
          })
        };
        wx.showToast({
          title: res.data.msg,
          icon:'none'
        })
      }
    })

  },
  intoIndex(){
    wx.redirectTo({
      url: '/pages/index/index',
    })
  }
})