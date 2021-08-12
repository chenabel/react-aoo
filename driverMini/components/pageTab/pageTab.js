// components/pageTab/pageTab.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    pageUrl:String
  },

  /**
   * 组件的初始数据
   */
  data: {
    url:"pages/personalCenter/personalCenter",
    homePageUrl:"pages/orderHall/orderHall"
  },

  /**
   * 组件的方法列表
   */
  methods: {
    backhome(e){
      if(this.data.homePageUrl == e.currentTarget.dataset.url)return
        wx.redirectTo({
          url: "../../" + this.data.homePageUrl
        })
    },
    goMyPage(e){
      if(this.data.url == e.currentTarget.dataset.url)return
      wx.redirectTo({
        url: "../../" + this.data.url,
      })
    },
  }
})
