// pages/myOrder/myOrder.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    pageToHeight:app.globalData.pageToHeight,
    paddingTopNum:app.globalData.paddingTopNum,
    isReachEnd:false,
    currentPage:1,
    perPage:5,
    ordersArr:[],
    totalPage:1,

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    if (this.data.currentPage < this.data.totalPage){
      this.data.currentPage++;
    }else{
      this.setData({
        isReachEnd:true,
      })
      return
    }
    this._getList()
  },
  _getList(){
    // 发送请求之前 ： 都会有一个加载框
    wx.showLoading({
      title: '玩命加载...',
    })
    wx.request({
      url: app.host +'api/checkMyoder/?token='+wx.getStorageSync('token'),
      data:{
        token:wx.getStorageSync('token'),
        currentPage:this.data.currentPage,
        perPage:this.data.perPage
      },
      success:(res)=>{
          if(res.data.id>=0){
            // 把新的数据添加到 旧的后面
            const l = this.data.ordersArr.concat(res.data.datas);
            const t = Math.ceil(res.data.id / this.data.perPage)
            
            this.setData({
              ordersArr:l,
              totalPage:t
            })
            console.log(this.data.ordersArr);
          }
          else{
             wx.showToast({
               title: res.data.msg,
               icon:'none'
             })
             setTimeout(() => {
              wx.redirectTo({
                url: '/pages/loginPage/login',
              })
             }, 1000);
          }     
      },
      complete(){
        wx.hideLoading()
      }
    })
  },
  onLoad(){
    // 分页 触底加载更多
    // 要发送什么参数？ （第几页，每页多少条）（开始，结束） token
    this._getList()
  },
  intoIndex(){
    wx.redirectTo({
      url: '../user/index',
    })
  },

  // 司机信息
  getDriverInfos(e){
    let current = e.currentTarget.dataset.current 
    // console.log(current);
    let drivers = this.data.ordersArr[current].driver_id
    // console.log(drivers);
    wx.showModal({
      title: '司机信息',
      content: drivers.driver_name.substr(0,1)+"师傅"+'\r\n'+drivers.driver_plate+'\r\n'+drivers.driver_carbrand+'\r\n'+drivers.driver_cartype+'\r\n'+drivers.driver_tel,
    })
  },
  // 支付
  pay(e){
    let current = e.currentTarget.dataset.current 
    let oid = this.data.ordersArr[current].order_id
    let price = this.data.ordersArr[current].order_price
   
    wx.showModal({
      title:'支付窗口',
      content:'请支付'+price+'元',
      success(res){
         if(res.confirm){
            wx.request({
              url: app.host+'api/myorderPay/?token='+wx.getStorageSync('token'),
              data:{
                oid:oid,
                price:price
              },
              success:resp=>{
                if(resp.data.id==1){
                   wx.showToast({
                     title: resp.data.msg,
                     icon:'none'
                   })
                   
                }else{
                  wx.showToast({
                    title: resp.data.msg,
                    icon:'none'
                  })
                  setTimeout(() => {
                    wx.redirectTo({
                      url: '../myWallet/myWallet',
                    })
                  }, 2000);
                }
              }
            })
           
         }
      }
    })
  }
})