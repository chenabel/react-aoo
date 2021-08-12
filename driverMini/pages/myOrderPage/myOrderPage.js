const app = getApp()
Page({
  data: {
    headHeight: (wx.getSystemInfoSync().statusBarHeight + 7) * 2 + 70,
    top:0,
    orderList: [{
      order_price: 987, // 订单价格
      order_startadd: '福州市仓山区大榕树文化创意园', // 出发地 
      order_destadd: '上海浦东区黄埔东路古道街3号楼', // 目的地
      order_starttime: '2021-05-01 14:42',
      order_distance: '4.5km',
      order_id: "1123",
      order_state:"已完成"
    },{
      order_price: 987, // 订单价格
      order_startadd: '福州市仓山区大榕树文化创意园', // 出发地 
      order_destadd: '上海浦东区黄埔东路古道街3号楼', // 目的地
      order_starttime: '2021-05-01 14:42',
      order_distance: '4.5km',
      order_id: "1123",
      order_state:"已完成"
    },{
      order_price: 987, // 订单价格
      order_startadd: '福州市仓山区大榕树文化创意园', // 出发地 
      order_destadd: '上海浦东区黄埔东路古道街3号楼', // 目的地
      order_starttime: '2021-05-01 14:42',
      order_distance: '4.5km',
      order_id: "1123",
      order_state:"已完成"
    },{
      order_price: 987, // 订单价格
      order_startadd: '福州市仓山区大榕树文化创意园', // 出发地 
      order_destadd: '上海浦东区黄埔东路古道街3号楼', // 目的地
      order_starttime: '2021-05-01 14:42',
      order_distance: '4.5km',
      order_id: "1123",
      order_state:"已完成"
    },{
      order_price: 987, // 订单价格
      order_startadd: '福州市仓山区大榕树文化创意园', // 出发地 
      order_destadd: '上海浦东区黄埔东路古道街3号楼', // 目的地
      order_starttime: '2021-05-01 14:42',
      order_distance: '4.5km',
      order_id: "1123",
      order_state:"已完成"
    },{
      order_price: 987, // 订单价格
      order_startadd: '福州市仓山区大榕树文化创意园', // 出发地 
      order_destadd: '上海浦东区黄埔东路古道街3号楼', // 目的地
      order_starttime: '2021-05-01 14:42',
      order_distance: '4.5km',
      order_id: "1123",
      order_state:"已完成"
    }]
  },
  onShow(){
    wx.request({
      url:app.globalData.host + 'api/driver/getMyOrder/',
      data:{
        openId:wx.getStorageSync('openid')
      },
      method:'post',
      success:res=>{
        this.setData({
          orderList:res.data.driver
        })
      }
    })
  },
  clickOrder(e){
    console.log(e)
    app.globalData.orderId = e.currentTarget.dataset.oid
    wx.redirectTo({
      url: '/pages/orderPage/orderPage',
    })
  }
})