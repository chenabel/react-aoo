// pages/addEndaddress/add.js
const app = getApp()
const QQMapWX = require('../libs/qqmap-wx-jssdk.js');
var qqmapsdk;
Page({
    
  /**
   * 页面的初始数据
   */
  data: {
    pageToHeight:app.globalData.pageToHeight,
    paddingTopNum:app.globalData.paddingTopNum,
    destAddressList:[],
    city:''
  },
  changeCity(){
    wx.setStorageSync('currcity',this.data.city)
    wx.redirectTo({
      url: '../changeCity/changeCity',
    })
  },
  onLoad(){ 
    qqmapsdk = new QQMapWX({
      key: 'CJZBZ-R5DKR-WQ7WT-WU3BY-SCWF2-DIBDW'
    })
    const currcity=wx.getStorageSync('currcity')
    if(currcity===""|| currcity===undefined){
      wx.getLocation({
        type: 'gcj02',
        success:res=>{
          console.log(res.latitude,res.longitude)
          qqmapsdk.reverseGeocoder({
            location: {
              latitude: res.latitude,
              longitude: res.longitude
            },
            success:res =>{
              let city=res.result.address_component.city
              this.setData({
                city:city
              })
              this.destChange(city)
            }
          })
        }
      })
    }else{
      this.setData({
        city:currcity
      })
      this.destChange(currcity)
      wx.setStorageSync('currcity','')
    }
  },
  destChange(e) {
    //调用关键词提示接口
    var keyword=''
    if(typeof(e)=='string'){
      keyword=e
    }else{
      keyword=this.data.city+e.detail.value
    }
    qqmapsdk.getSuggestion({
      keyword:keyword,
      success: res=>{
        var sug = [];
        for (var i = 0; i < res.data.length; i++) {
          sug.push({
            title: res.data[i].title,
            id: res.data[i].id,
            addr: res.data[i].address,
            city: res.data[i].city,
            district: res.data[i].district,
            latitude: res.data[i].location.lat,
            longitude: res.data[i].location.lng
          });
        }
        this.setData({ //设置suggestion属性，将关键词搜索结果以列表形式展示
          destAddressList: sug
        });
      },
      fail: function(error) {
        console.error(error);
      },
      complete: function(res) {
        console.log(res);
      }
    });
  },
  clickAdd(e){
    wx.setStorageSync('destAddress', e.currentTarget.dataset.address)
    wx.redirectTo({
      url:'../index/index'
    })
  },
  intoIndex(){
    wx.redirectTo({
      url: '../index/index',
    })
  }
})