const app = getApp()
var QQMapWX = require('../../common/js/qqmap-wx-jssdk.js');
var qqmapsdk = new QQMapWX({
  key: 'LMLBZ-CFF3F-GHWJF-NWEAP-N7OCQ-VFFZU' // 必填
});
const innerAudioContext = wx.createInnerAudioContext();
innerAudioContext.src = "/mp3/wrongRoute.mp3"
var webSocket = false
Page({
  data: {
    headHeight: (wx.getSystemInfoSync().statusBarHeight + 7) * 2 + 70,
    orderId: "", // 订单id
    orderInfo: {},
    polyline: [],//路线渲染
    latitude: 0,//纬度
    longitude: 0,//经度
    chat: false,
    chatcontent: "",
    //标记点
    markers: [],
    form: [],
    fromLng: "",// 司机当前位置经度
    fromLat: "",// 司机当前位置纬度
    orderBegin: "",//订单起点
    orderEnd: "",//订单终点
    orderInfoHeight: "",//orderInfoHeight高度
    msgs: [],
    MikeBox: "",
    animationData: "",
    animationData2: "",
    chooseSize: true,
    angle: 180,
    distance: "0km",
    isUserFlag:false,
    chat:false,
    textValue: "",//司机输入的话
    top:"",
  },
  
  chat() {
    if (this.data.chat === false) {
      this.data.chat = true
    } else {
      this.data.chat = false
    }
    this.setData({
      chat: this.data.chat
    })
  },

  onLoad() {
    this.getPosition()
    const _this = this;
    var myDate = new Date();
    wx.connectSocket({
      url: 'ws://127.0.0.1:8000/',
      header:{
        'content-type':'application/json'
      },
      success:function(res){
        console.log(res)
        console.log("客户端连接成功")
        wx.onSocketOpen(function(){
          console.log('webSocket已打开！')
          webSocket = true
          _this.sendMessage()
          wx.onSocketMessage(function(resp){
            var data = JSON.parse(resp.data)
              var obj = {
                msgTent: data.content.msg,
                msgTime: (myDate.getHours() >= 10 ? myDate.getHours():"0"+myDate.getHours())+ ":" + (myDate.getMinutes() >= 10 ? myDate.getMinutes(): "0" + myDate.getMinutes()),
                msgName: (data.content.who == "driver" ? "我":"乘客"),
                from:data.content.who
              }
            var temp = _this.data.msgs
            var len = _this.data.msgs.length
            temp.push(obj)
            console.log(data) 
            console.log(typeof(data)) //对象
            console.log(_this.data.msgs)
            if( data.content.msg != ""){
              _this.setData({
                msgs: temp,
                top: len * 1000
              })
            }
            console.log(_this.data.top)
          })
          wx.onSocketClose(function(){
            console.log('webSocket已关闭！');
          })
        })
      },
      complete:function(err){
        console.log(err)
      }
    })
  },

  onShow() {
    console.log(this.data.headHeight)
    this.getOrderData()
    innerAudioContext.src = "../../mp3/wrongRoute.mp3"
    if(app.globalData.isDisconnection == true) {
      this.IamHere()
    }
  },

  getPosition() {
    //获得司机当前位置
    var that = this;
    wx.getLocation({
      type: 'gcj02',
      success: function (res) {
        that.setData({
          fromLng: res.longitude,
          fromLat: res.latitude
        })
        // that.getOrderData()
      }
    })
  },

  getOrderData() {
    var that = this
    wx.request({
      url: app.globalData.host + 'api/driver/getOrderData/',
      data: {
        oid: app.globalData.orderId
      },
      method: 'post',
      success(res) {
        that.setData({
          orderInfo: res.data.order
        })
        that.getAddRess(that.data.orderInfo.order_startadd)
        that.getAddRess(that.data.orderInfo.order_destadd)
      }
    })
  },

  getAddRess(add) {
    var that = this
    qqmapsdk.geocoder({
      address: add,
      success: function (res) {
        var temp = that.data.form
        temp.push(res.result.location.lat + "," + res.result.location.lng)
        that.setData({
          form: temp
        })
        if (that.data.form.length == 1) {
          that.setData({
            "markers[0].longitude": res.result.location.lng,
            "markers[0].latitude": res.result.location.lat
          })
        } else if (that.data.form.length == 2) {
          that.setData({
            "markers[1].longitude": res.result.location.lng,
            "markers[1].latitude": res.result.location.lat
          })
        }
        var from = that.data.fromLat + "," + that.data.fromLng
        that.getRoute(from, that.data.form[0])
      }
    })
  },

  getRoute(begin, end) {
    var that = this
    if (that.data.form.length != 2) return
    qqmapsdk.direction({
      mode: 'driving',
      from: begin,
      to: end,
      success: function (res) {
        var ret = res;
        var coors = ret.result.routes[0].polyline, pl = [];
        //坐标解压（返回的点串坐标，通过前向差分进行压缩）
        var kr = 1000000;
        for (var i = 2; i < coors.length; i++) {
          coors[i] = Number(coors[i - 2]) + Number(coors[i]) / kr;
        }
        //将解压后的坐标放入点串数组pl中
        for (var i = 0; i < coors.length; i += 2) {
          pl.push({ latitude: coors[i], longitude: coors[i + 1] })
        }
        //设置polyline属性，将路线显示出来,将解压坐标第一个数据作为起点
        that.setData({
          latitude: pl[0].latitude,
          longitude: pl[0].longitude,
          polyline: [{
            points: pl,
            color: "#20B2AA", width: 4, dottedLine: false
          }]
        })
        let count=0
        const lineArr=that.data.polyline[0].points
        var Interval=setInterval(() => {
          if(lineArr.length>=1){
            var rota=that.getAngle(lineArr[0].longitude,lineArr[0].latitude,lineArr[1].longitude,lineArr[1].latitude)
          }
          let markers={
            iconPath: "/images/car.png",
            id: 2,
            latitude: lineArr[0].latitude,
            longitude: lineArr[0].longitude,
            width: 32,
            height: 32,
            rotate: rota
          }
          if(count===0){
            that.data.markers.push(markers)
          }else{
            lineArr.shift()
            that.data.markers.pop()
            that.data.markers.push(markers)
          }
          that.setData({
            markers:that.data.markers,
            polyline:that.data.polyline
          })
          const text={
            msg:that.data.polyline,
            markers:markers,
            orderid:app.globalData.orderId,
            serviceType:'sendLocation',
            from:'driver',
          }
          wx.sendSocketMessage({
            data: JSON.stringify(text),
          })
          if(lineArr.length<=1){
            clearInterval(Interval)
          }
          count++;
        },1000)
      }
    });
  },
  getAngle(lng_a, lat_a, lng_b, lat_b) {
    let y = Math.sin(lng_b - lng_a) * Math.cos(lat_b);
    let x =
    Math.cos(lat_a) * Math.sin(lat_b) -
    Math.sin(lat_a) * Math.cos(lat_b) * Math.cos(lng_b - lng_a);
    let angle= Math.atan2(y, x);
    angle= (180 * angle) / Math.PI;
    return angle
  },
  regionchange(e) {
    
  },

  IamHere() {
    //点击后  将切换为将用户标记点当为终点
    wx.showModal({
        title: '',
        content: '是否确定已经接到乘客！',
        success:  res=> {
         if (res.confirm) {
          wx.showToast({
            title: '已为您规划路线！',
          })
          const text={    
            orderid:app.globalData.orderId,
            serviceType:'alreadyGetPassenger',
            from:'driver'
          }
          wx.sendSocketMessage({
            data: JSON.stringify(text),
          })
          this.getOrderData()
          this.getRoute(this.data.form[0], this.data.form[1])
          innerAudioContext.play()
          this.setData({
            isUserFlag:true
          })
          this.getDistance()

        }
      }
    })
  },
  
  userOutCar(e) {
    wx.showModal({
      title:"",
      content:"是否确定已到达目的地点！",
      success:res=>{
        if (res.confirm) {
          wx.request({
            url: app.globalData.host + 'api/driver/getUser/',
            data: {
              oid: app.globalData.orderId,
              type: "outUser",
            },
            method: 'post',
            success(res) {
              wx.showToast({
                title: res.data.msg,
                icon: res.data.type,
              })
              setTimeout(function(){
                wx.redirectTo({
                  url: '/pages/orderHall/orderHall',
                })
              },2000)
            }
          })
        }
      }
    })
  },

  handEnd(e) {
    var fristTab = this.data.MikeBox
    var endNum = e.changedTouches[0].pageY
    var that = this
    var animation = wx.createAnimation({
      duration: 500,
      timingFunction: 'linear'
    })
    var animation2 = wx.createAnimation({
      duration: 500,
      timingFunction: 'linear'
    })
    that.animation2 = animation2
    that.animation = animation
    if (fristTab > endNum + 30) {
      animation.translateY(-270).step()
      animation2.rotate(0).step()
      this.setData({
        animationData: animation.export(),
        animationData2: animation2.export(),
        chooseSize: true,
      })
    } else if (fristTab < endNum && fristTab != '') {
      // 先在y轴偏移，然后用step()完成一个动画
      animation.translateY(0).step()
      animation2.rotate(180).step()
      this.setData({
        animationData: animation.export(),
        animationData2: animation2.export(),
        chooseSize: true,
      })
    }
    this.setData({
      MikeBox: ""
    })
  },

  handletouchmove(e) {
    var temp = []
    temp.push(e.changedTouches[0])
    if (this.data.MikeBox.length == 0) {
      this.setData({
        MikeBox: temp[0].pageY
      })
    }
  },

  inputText(e) {
    this.setData({
      textValue: e.detail.value
    })
  },

  getDistance() {
    var that = this
    wx.request({
      url: 'https://apis.map.qq.com/ws/geocoder/v1/',
      data: {
        "key": "LMLBZ-CFF3F-GHWJF-NWEAP-N7OCQ-VFFZU",
        "address": this.data.orderInfo.order_destadd //this.data.orderInfo.order_destadd
      },
      method: 'GET',
      success: function (res) {
        if (res.data.result) {
          const addressLocation = res.data.result.location;
          const courseLat = addressLocation.lat;
          const courseLng = addressLocation.lng;
          let destinationDistance;
          qqmapsdk.calculateDistance({
            to: [{
              latitude: courseLat,
              longitude: courseLng
            }],
            success: function (res) {
              destinationDistance = res.result.elements[0].distance;
              let distanceKm = `${(destinationDistance / 1000).toFixed(2)}Km`;//转换成km
              that.setData({
                distance: distanceKm
              })
            },
            fail: function (res) {

            }
          });
        }
      }
    })
  },

  sendMessage(){
    var myDate = new Date();
    var that = this
    const text={
      msg:that.data.textValue,
      orderid:app.globalData.orderId,
      serviceType:'sendMsg',
      from:'driver',
    }
    console.log(that.data.textValue)
    // if(that.data.textValue == '')return
    if(webSocket){
      wx.sendSocketMessage({
        data: JSON.stringify(text),
      })
      that.setData({
        chatcontent:'',
        scrollTop:that.data.msgs.length * 1000
      })
    }
    that.data.textValue = ''
  },
})


