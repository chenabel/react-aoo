//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {}
  },

  goToIndex: function() {
    var openid = wx.getStorageSync('openid')
    console.log(openid)
    wx.request({
      url: app.globalData.host+'api/driver/selectDriverOpenid/',
      data:{
        openid:openid
      },
      success(res){
        console.log(123)
        if(res.data.type != "error"){
          wx.navigateTo({
            url: "../../" + res.data.location,
          })
        }else{
          wx.navigateTo({
            url: "../../" + res.data.location,
          })
        }
      }
    })
  },

  onLoad: function() {
  // 获取openid
  var that = this;
  wx.login({
    success(res) {
      console.log(res)
      var appid = app.globalData.appid
      var secret = app.globalData.secret
      var code = res.code
      wx.request({
        url: 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code',
        success(res1) {
          console.log(res1)
          wx.setStorageSync('openid', res1.data.openid)
          wx.setStorageSync('session_key', res1.data.session_key)
          that.setData({
            openid: res1.data.openid
          })
        }
      })
    }
  })
  },

  onShow: function() {
    let that = this
    let userInfo = wx.getStorageSync('userInfo')
    if (!userInfo) {
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
          })
          console.log(app.globalData.userInfo)
        }
      })
    } else {
      that.setData({
        userInfo: userInfo
      })
    }
  },
  
  onReady: function() {
    var that = this;
    setTimeout(function() {
      that.setData({
        remind: ''
      });
    }, 1000);
    wx.onAccelerometerChange(function(res) {
      var angle = -(res.x * 30).toFixed(1);
      if (angle > 14) {
        angle = 14;
      } else if (angle < -14) {
        angle = -14;
      }
      if (that.data.angle !== angle) {
        that.setData({
          angle: angle
        });
      }
    });
  }
});