const app = getApp()
var QQMapWX = require('../../common/js/qqmap-wx-jssdk.min');
// 实例化API核心类
var qqmapsdk = new QQMapWX({
  key: '地图key' // 必填
});
Page({
  data: {
    headHeight: (wx.getSystemInfoSync().statusBarHeight + 7) * 2 + 70,
    orderList: {
      order_passenger: "L",
      order_startadd: "福建省福州市仓山区闽江大道236号",
      order_destadd: "福建省福州市长乐漳湖路6号",
      order_pretime: "今天15点",
      order_price: "99",
      order_distance: "47.173",
      order_id: "1",
      order_tel: "13665093859",
    },
  },
  onLoad() {
    var that = this
    wx.request({
      url: app.globalData.host + 'api/driver/getOrderInfo/',
      data: {
        orderId: app.globalData.orderId,
      },
      method: 'post',
      success(res) {
        that.setData({
          orderList: res.data.orderInfo
        })
        wx.showModal({
          title: '请确定乘客手机尾号',
          content: res.data.userTel,
          showCancel: false,  // 不显示取消按钮
          success(res) {
            if (res.confirm) {
              console.log('用户点击确定')
            } else if (res.cancel) {
              console.log('用户点击取消')
            }
          }
        })
      }
    })
  },
  getUser(e) {
    console.log(e)
    wx.request({
      url: app.globalData.host + 'api/driver/getUser/',
      method: 'post',
      data: {
        oid: e.currentTarget.dataset.oid,
        type: "getUser"
      },
      success() {
        app.globalData.orderId = e.currentTarget.dataset.oid
        wx.navigateTo({
          url: '../../pages/orderPage/orderPage',
        })
      }
    })
  }
})