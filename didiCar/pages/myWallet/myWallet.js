// pages/myWallet/myWallet.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    pageToHeight:app.globalData.pageToHeight,
    paddingTopNum:app.globalData.paddingTopNum,
    openeyes:true,
    closeeyes:false,
    money:true,
    hidemoney:false,
    moneynum:0.00,
    recharge:false
  },
  onLoad(){
      this.showMoney();
  },
  showMoney(){
    wx.request({
      url: app.host+'api/checkMoney/?token='+wx.getStorageSync('token'),
      success:res=>{
         if(res.data.id == 1){
           this.setData({
             moneynum:res.data.datas
           })
         }else{
             wx.showToast({
               title: res.data.msg,
               icon:"none"
             })
             setTimeout(() => {
              wx.redirectTo({
                url: '../loginPage/login',
              })
             }, 2000);
             
         }
      }
    })
  },

  intoIndex(){
     wx.redirectTo({
       url: '../user/index',
     })
  },
  closeEyes(){
    this.setData({
        openeyes:false,
        closeeyes:true,
        money:false,
        hidemoney:true,
    })
  },
  openEyes(){
    this.setData({
        openeyes:true,
        closeeyes:false,
        money:true,
        hidemoney:false,
        inputMoney:''
  })
  },
  recharge(){
    this.setData({
      recharge:true
     })
  },
  closeRecharge(){
     this.setData({
      recharge:false
     })
  },
  getMoney(e){
    let money = e.detail.value;
    this.setData({
      inputMoney:money
    })
  },
  confirm(){
    if(!/^[0-9]*$/.test(this.data.inputMoney)){
      wx.showToast({
        title: '请输入正确数字！',
        icon:"none",
        duration:2000,
      })
      return;
    }
    wx.request({
      url: app.host+'api/addMoney/?token='+wx.getStorageSync('token'),
      data:{
         money:this.data.inputMoney
      },
      success:res=>{
        if (res.data.id == 1) {
          wx.showToast({
            title: '充值成功！',
            icon:"none"
          });
          this.setData({
            recharge:false
          })
          this.showMoney();
        }else{
          wx.showToast({
            title: res.data.msg,
            icon:"none"
          })
          wx.redirectTo({
            url: '../loginPage/login',
          })
        }
      }
    })
  }

})