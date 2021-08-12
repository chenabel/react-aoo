Component({
  data:{
      paddingTopNum:wx.getSystemInfoSync().statusBarHeight+7
  },
  properties: {    
    pageName: String  
  },
  methods:{
    _navback() {
      var pages = getCurrentPages(); //当前页面
      var beforePage = pages[pages.length - 2]; //前一页
      wx.navigateBack({
        success: function () {
          beforePage.onLoad(); // 执行前一个页面的onLoad方法
        }
      });
      console.log('我退回原页面了',beforePage)
    },
    _backhome() {
      wx.navigateTo({
        url: '/pages/index/index',
      })
    },
  },
  
})