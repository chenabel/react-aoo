// pages/changePerson/person.js
const app = getApp()
Page({
    
  /**
   * 页面的初始数据
   */
  data: {
    pageToHeight:app.globalData.pageToHeight,
    passengerName:'',
    passengerTel:'',
    passengerList:[],
  },
  onLoad(){
    wx.request({
      url: app.host+'api/checkHispassenger/?token='+wx.getStorageSync('token'),
      data:{
        token:wx.getStorageSync('token')
       },
       success:res=>{
          if (res.data.id==1) {
            this.setData({
              passengerList:res.data.datas
            })
          }else{
            wx.showToast({
              title: res.data.datas,
              icon:"none"
            });
            setTimeout(() => {
              wx.redirectTo({
                url: '/pages/loginPage/login',
              })
            }, 1000);
          }
       }
    })
  },

  intoIndex(){
    wx.redirectTo({
      url: '../index/index',
    })
  },
  inputName(e){
    this.setData({
      passengerName:e.detail.value
    })
  },
  inputTel(e){
    this.setData({
      passengerTel:e.detail.value
    })
  },
  confirm(){
    if(!/^1[3456789]\d{9}$/.test(this.data.passengerTel)){
      wx.showToast({
        title: '手机号码输入有误！',
        icon:'none',
        duration:2000,
      })
      return;
    }
    wx.request({
      url: app.host+'api/addPassenger/?token='+wx.getStorageSync('token'),
      data:{
          passengerName:this.data.passengerName,
          passengerTel:this.data.passengerTel,
          token:wx.getStorageSync('token')
      },
      success:res=>{
         if(res.data.id==1){
            wx.setStorageSync('passengerTel', this.data.passengerTel)
            wx.setStorageSync('passengerName', this.data.passengerName)
            wx.redirectTo({
              url: '/pages/index/index',
            })
         }else{
           wx.redirectTo({
             url: '/pages/loginPage/login',
           })
         }
      }
    })
  },
  optionPassenger(e){
     const index = e.currentTarget.dataset.curindex
     console.log(this.data.passengerList[index]);
     wx.setStorageSync('passengerTel', this.data.passengerList[index].historypassenge_tel)
     wx.setStorageSync('passengerName',this.data.passengerList[index].historypassenge_name)
     wx.redirectTo({
        url: '/pages/index/index',
      })

  }
})