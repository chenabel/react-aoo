Component({
  properties: {
  },
  data: {
    showTopTips: true,
    msg: '提示'
  },
  methods: {
    showDialog(msg) {
      wx.showModal({
        title: '提示',
        content: msg,
      })
    },
    showTopTip: function(msg) {
      let that = this;
      that.setData({
        showTopTips: false,
        msg: msg
      });
      // setTimeout(function() {
      //   that.setData({
      //     showTopTips: true
      //   });
      // }, 2000);
    }
  }
})