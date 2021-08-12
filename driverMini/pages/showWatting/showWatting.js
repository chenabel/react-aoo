// pages/showWatting/showWatting.js
Page({
  data: {
  },
  onLoad: function (options) {
    wx.showModal({
      title: '',
      content: "请耐心等待信息审核,结果将于一个工作日后公众号查看！",
      showCancel: false,  // 不显示取消按钮
    })
  }
})