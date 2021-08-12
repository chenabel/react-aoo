// index.js
// 获取应用实例
const app = getApp()
var toptips;
Page({
  data: {
    twoBtnFlage: {
      banckground: "white",
      color: '#ff7e33',
      display: 'block',
      border: '1rpx solid #ff7e33'
    },
    twoBtnFlage2: {
      banckground: '#f3f3f3',
      color: '#646466',
      display: "none",
      border: '1rpx solid #dcdcdc'
    },
    isTwoBtnFlage: false,
    nowAdd: '',
    telNum: '', // 用户输入的电话号码
    isTelNum: false, // 判断用户输入的电话号码长度够不够
    isTelNum2: false,// 如果用户输入的电话不符合正则也是错的
    error: '',
    showTopTips: false,
    msg: '',
    isCheckBox: false,  // 点击了同意条框
    getCodeText: '获取短信验证码',
    second: 60, // 倒计时用的
    openTimeing: false, // 判断定时器是否存在 如果存在为 false
    code: '', // 用户输入的验证码
    isTelNum3: '', // 用户输入的验证码不能为空
    isTelNum4: '', // 司机所在城市不能为空
    driverCarType: 1, // 司机的车是自己有为1 租的为2
    openid:"",
    headHeight:(wx.getSystemInfoSync().statusBarHeight+7)*2 + 70,
  },
  
  onLoad(){
    // 获取openid
    var that = this;
    this.selectUserOpenId()
  },
  
  onReady(){
    this.getAddFoo()
  },

  selectUserOpenId(){
    var openid = wx.getStorageSync('openid')
    this.setData({
      openid:openid
    })
    wx.request({
      url: app.globalData.host+'api/driver/selectDriverOpenid/',
      data:{
        openid:openid
      },
      success(res){
        if(res.data.type != "error"){
          wx.navigateTo({
            url: "../../" + res.data.location,
          })
        } 
      }
    })
  },

  // 把输入的电话号码存入app 里头 
  inText(e){
    app.globalData.tel = e.detail.value
  },

  onShow() {
    // 用户显示用户选择了 城市后 index 页面也显示 这个城市
    var that = this
    this.setData({
      nowAdd: app.globalData.cityName,
      // 给输入框赋入点击城市选择之前输入的电话
      telNum:app.globalData.tel
    })
  },

  goLoginPage() {
    wx.redirectTo({
      url: '../../pages/login/login',
    })
  },

  goResgister() {
    wx.redirectTo({
      url: '../../pages/resgister/resgister',
    })
  },

  iHaveCar() {
    if (this.data.isTwoBtnFlage == false) {
      this.setData({
        twoBtnFlage: {
          banckground: '#f3f3f3',
          color: '#646466',
          display: "none",
          border: "1rpx solid #dcdcdc"
        },
        twoBtnFlage2: {
          banckground: "white",
          color: '#ff7e33',
          display: 'block',
          border: '1rpx solid #ff7e33'
        },
        isTwoBtnFlage: true
      })
    } else {
      this.setData({
        twoBtnFlage2: {
          banckground: '#f3f3f3',
          color: '#646466',
          display: "none",
          border: '1rpx solid #dcdcdc'
        },
        twoBtnFlage: {
          banckground: "white",
          color: '#ff7e33',
          display: 'block',
          border: '1rpx solid #ff7e33'
        },
        isTwoBtnFlage: false
      })
    }
  },

  cityChooese(){
    wx.redirectTo({
      url: '/pages/chooseCity/chooseCity',
    })
  },

  getAddFoo() {
    if(this.data.nowAdd == ''){
      wx.getLocation({
        type: 'gcj02',
        success: (res) => {
          var that = this
          var QQMapWX = require('../../common/js/qqmap-wx-jssdk.js');         
          var qqmapsdk = new QQMapWX({
              key: 'JNFBZ-VY6CJ-SSLFY-KNTXW-WJ32F-IXB5X' 
          });  
          qqmapsdk.reverseGeocoder({
            location: {
              latitude: res.latitude,
              longitude: res.longitude
            },
            success: function(res) {//成功后的回调
              that.setData({
              nowAdd:res.result.address_component.city
              })
              console.log(that.data.nowAdd)
            },
          })
        }
      })
    }
  },

  inputTelNum(e) {
    var myreg = /^1(3|4|5|6|7|8|9)\d{9}$/;
    this.setData({
      telNum: e.detail.value,
    })
    if (e.detail.value.length == 11) {
      this.setData({
        isTelNum: false
      })
    } else {
      this.setData({
        isTelNum: true
      })
    }
    if (!myreg.test(this.data.telNum)) {
      this.setData({
        isTelNum2: true
      })
    } else {
      this.setData({
        isTelNum2: false
      })
    }
  },

  getCode() {
    var that = this
    // 如果定时器开着 就不让再生成 定时器了
    if (this.data.openTimeing == true) return
    if (this.data.telNum.length == 11) {
      // 如果用户输入的是 12开头或者11 开头 或者10开头 是不符合规则的 inputTelNum 控制着用户输入的 电话是不是对的
      // 如果是对的就改编 isTelNum2规则  和 isTelNum 电话长度
      if (this.data.isTelNum2 == true) {  // 判断是否符合正则规则
        this.setData({
          isTelNum2: true
        })
        // 不符合规则打断 
        return
      }
      wx.request({
        url: app.globalData.host + 'api/driver/getCode/',
        data: {
          telNum: this.data.telNum
        },
        method: 'post',
        success(res) {
          wx.showToast({
            title: res.data.msg,
            icon: res.data.type,
            duration: 1500
          })
        }
      })
      var second = this.data.second // 设置定时器的秒数  
      var timeing = setInterval(function () { // 取了一个 教timeing的定时器 关闭的时候会用到
        that.setData({
          openTimeing: true, // 表示着 这个定时器 已经开过了
          getCodeText: second - 1 + '秒'
        })
        second = second - 1
        // 定时器时间倒计时为0了 打断进程恢复可以点击的状态
        if (second == 0) {
          that.setData({
            getCodeText: '获取短信验证码',
            openTimeing: false,
          })
          clearInterval(timeing)
        }
      }, 1000)
    } else {
      // 如果用户输入的电话长度不够，提示出长度不够的提示。
      this.setData({
        isTelNum: true
      })
    }
  },

  checkboxFee() {
    this.setData({
      isCheckBox: this.data.isCheckBox == true ? false : true,
    })
  },

  inputCode(e) {
    this.setData({
      code: e.detail.value
    })
  },

  doResgister() {
    var that = this
    if (this.data.telNum == '') {
      this.setData({
        isTelNum5: true
      })
      return
    } else {
      this.setData({
        isTelNum5: false
      })
    }
    // 如果所在城市为空，提示 并打断
    if (this.data.nowAdd == '') {
      wx.showToast({
        title: '所在城市不为能为空',
        icon: 'none'
      })
      return
    }
    if (this.data.isCheckBox == true) {
    // 是否点击了 同意《加入滴滴的条件说明和承诺》 
   
    // 用户没输入验证码，提示 并打断 
    if (this.data.code == '' || this.data.code == null) {
      this.setData({
        isTelNum3: true
      })
      return
    } else {  // 不为空就去调用说明就取消那个提示 
      this.setData({
        isTelNum3: false
      })
    }
      wx.request({
        url: app.globalData.host + 'api/driver/doResgister/',
        data: {
          telNum: this.data.telNum,
          code: this.data.code,
          cityName: this.data.nowAdd,
          driverCarType: this.data.driverCarType,
          openId:this.data.openid
        },
        method: 'post',
        success: function (res) {
          console.log(res)
          if (res.data.type == 'success') {
            wx.redirectTo({
              url: '/pages/tipPages/tipPages',
            })
          } else {
            wx.showToast({
              title: res.data.msg,
              icon: res.data.type,
              duration: 1500
            })
          }
          app.globalData.driverTel = that.data.telNum
        }
      })
    } else {
      wx.showToast({
        title: '请先阅读并同意《加入滴滴的条件和承诺》',
        icon: 'none',
        duration: 1500
      })
    }
  }
})

