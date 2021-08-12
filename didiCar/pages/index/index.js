// index.js
// 获取应用实例
const app = getApp()
const QQMapWX = require('../libs/qqmap-wx-jssdk.js');
var qqmapsdk;
Page({
   data: {
      pageToHeight:app.globalData.pageToHeight,
      menuList: [{
        name: "快车"
      }, {
        name: "专车"
      }, {
        name: "顺风车"
      }, {
        name: "出租车"
      }, {
        name: "代驾"
      }],
      carTypeList:["普通型","优享型"],
      tabScroll: 0,
      currentTab: 0, //导航栏初始化为0
      windowHeight: '',
      windowWidth: '',
      tabState:0,//导航状态
      currentCarType:0,//车子类型
      currentCarOpt:'普通型',//车子选择
      // 快车picker
      multiArray: [['今天', '明天', '后天'], []],
      multiIndex: [0, 0],
      normalHours: [],
      todayHours: [],

      // 顺风车picker
      hitchArray: [],
      hitchIndex:[0,0,0],
      firstHitchTime:'',
      lastHitchTime:'',

      startlatitude:'',//开始维度
      startlongitude:'',//开始经度
      startAddress:'',//开始地址
      destAddressList:'',//模糊查询列表
      polyline:'',//行驶路线
      destAddress:'',//终点地址
      destlongitude:'',//终点经度
      destlatitude:'',//终点维度
      isdest:false,//是否有终点
      distance:'',//起终距离
      nowtime:'',//初始时间
      price:'',//价格
      passenger:'',//乘车人
      passengertel:'',//乘车人手机
      passengerName:'',//乘车人名字
      showtel:'',
      hitchList:["乘客","车主"],//顺风车角色类型
      currentHitch:0 ,//当前顺风车角色
      passengerNumList: ['1人', '2人', '3人', '4人'],//顺风车人数列表
      passengerNumIndex:0,
      hitchOptNum:'',//顺风车选择人数
      hitchPrice:'',//顺风车价格
      showHitchPrice:''//顺风车前台显示价格
    },

    // 计算快车的价格
    countprice(index){
      let ko=(this.data.distance/1000).toFixed(1)
      if(index ===0){
        if(ko<3){
          this.data.price=11
        }else{
          this.data.price=((ko-3)*2+11).toFixed(2)
        }
      }else{
        if(ko<3){
          this.data.price=15
        }else{
          this.data.price=((ko-3)*3+15).toFixed(2)
        }
      }
      this.setData({
        price:this.data.price
      })
    },

    onLoad() { 
      // 获取目的地
      this.data.destAddress = wx.getStorageSync('destAddress');
      this.setData({
        destAddress:this.data.destAddress
      })
      console.log(this.data.destAddress)
      if(this.data.destAddress !==''){
        this.data.isdest = true;
      }else{
        this.data.isdest = false;
      }
      this.setData({
        isdest:this.data.isdest
      })
      qqmapsdk = new QQMapWX({
        key: 'CJZBZ-R5DKR-WQ7WT-WU3BY-SCWF2-DIBDW'
      });
      this.loadInfo();
      if(this.data.destAddress!=='' || this.data.destAddress!==undefined){
        //调用距离计算接口
        const destAddress=wx.getStorageSync('destAddress')
        qqmapsdk.geocoder({
          //获取表单传入地址
          address: destAddress, //地址参数，例：固定地址，address: '北京市海淀区彩和坊路海淀西大街74号'
          success:res=>{//成功后的回调
            console.log(this)
            this.data.destlongitude = res.result.location.lng;
            this.data.destlatitude = res.result.location.lat;
            const start=this.data.startlatitude+','+this.data.startlongitude
            const dest=this.data.destlatitude+','+this.data.destlongitude
            console.log(start,dest)
            const _this=this;
            qqmapsdk.direction({
              mode: 'driving',
              from:'',
              to:dest,
              success: function (res) {
                console.log(res);
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
                _this.setData({
                  latitude:pl[0].latitude,
                  longitude:pl[0].longitude,
                  polyline: [{
                    points: pl,
                    color: '#FF0000DD',
                    width: 4
                  }]
                })
              },
              fail: function (error) {
                console.error(error);
              },
              complete: function (res) {
                console.log(res);
              }
            });
            qqmapsdk.calculateDistance({
              mode: 'driving',
              from: '', //若起点有数据则采用起点坐标，若为空默认当前地址
              to: dest, //终点坐标
              success: function(res) {//成功后的回调
                var res = res.result;
                var dis = [];
                for (var i = 0; i < res.elements.length; i++) {
                  dis.push(res.elements[i].distance); //将返回数据存入dis数组，
                }
                dis=parseInt(JSON.stringify(dis).replace(/\[|]/g,''))
               
                _this.setData({ //设置并更新distance数据
                  distance:dis,
                });
                _this.countprice(0);
              },
              fail: function(error) {
                console.error(error);
              },
              complete: function(res) {
                console.log(res);
              }
          });
          }
        })
        
     // 获取当前设备的宽高，文档有
    wx.getSystemInfo({     
      success: (res) => { 
        this.setData({
          windowHeight: res.windowHeight,
          windowWidth: res.windowWidth
        })
      }
    })
    }

    // 换乘车人
     this.setData({
      passenger:wx.getStorageSync('passengerTel'),
      passengertel:wx.getStorageSync('passengerTel'),
      passengerName:wx.getStorageSync('passengerName')
     })

 
    },
    onReady(){
          this.hitchTime()
          this.setData({
            passenger:'尾号'+this.data.passenger.substring(7),
            showtel:this.data.passenger.substring(7)
          })
          
    },

     //  顺风车时间pick
    hitchTime(){
        var hitchArray = [['今天', '明天', '后天'],[],[]]
        for (let i = 7; i < 24; i++) {
          hitchArray[1].push(`${i}点`)
        }

        for (let i = 0; i < 60; i++) {
          if(i<10){
            var minStr = `0${i}分`
          }else{
            var minStr = `${i}分`
          }
          hitchArray[2].push(minStr)
        }
        this.setData({
          hitchArray:hitchArray
        })
       
    },
 

    
    // 获取当前定位
    loadInfo(){
      wx.getLocation({
        type: 'gcj02',
        success:res=>{
          this.data.startlatitude = res.latitude
          this.data.startlongitude = res.longitude
          qqmapsdk.reverseGeocoder({
            location: {
              latitude: this.data.startlatitude,
              longitude: this.data.startlongitude
            },
            success:res =>{
              this.data.startAddress=res.result.address
              this.setData({
                startAddress:this.data.startAddress
              })
            }
          })
          this.setData({
            startlatitude:this.data.startlatitude,
            startlongitude:this.data.startlongitude,
          })
        }
      })
    },
    // 获取车子类型
    optionCartype(e){
       let currentIndex = e.currentTarget.dataset.current;
       this.countprice(currentIndex);
       this.setData({
        currentCarType:currentIndex,
        currentCarOpt:this.data.carTypeList[currentIndex]
       })
    },
   
    // 点击顶部菜单
    clickMenu(e) {
      let current = e.currentTarget.dataset.current //获取当前tab的index
      let tabWidth = this.data.windowWidth / 5 // 导航tab共5个，获取一个的宽度
      this.setData({
        tabState:current,
        tabScroll: (current - 1) * tabWidth//使点击的tab始终在居中位置
        
      }) 
      if (this.data.currentTab == current) {
        return false
      } else {
        this.setData({currentTab: current })
      }
    },
    changeContent(e) {
      var current = e.detail.current   // 获取当前内容所在index
      var tabWidth = this.data.windowWidth / 5  
      this.setData({
        currentTab: current,
        tabScroll: (current - 2) * tabWidth
      })
    },
    //  跳转个人中心
    intoPerson(){
         const token = wx.getStorageSync('token');
         if(token == '' || token == undefined){
          wx.showToast({
            title: '请先登录',
            icon:'none',
          });
          setTimeout(function(){
            wx.redirectTo({
              url: '../loginPage/login',
            })
          },2000)
         }else{
           const usertel = wx.getStorageSync('usertel')
           if (usertel == '' || usertel == undefined){
                wx.showToast({
                  title: '您还未手机号绑定',
                  icon:'none',
                });
                setTimeout(function(){
                  wx.redirectTo({
                    url: '../phonePage/phone',
                  })
                },2000)
                return
           }
           wx.redirectTo({
             url: '../user/index',
           })
         }
         
    },
    // 时间选择
    initHour() {
      var hour = new Date().getHours();
      var todayHours = this.testConcat(hour); //根据当前小时生成数组
      var normalHours = this.testConcat(); //生成默认小时数组
      var multiArray = this.data.multiArray;
      multiArray[1] = todayHours; //初始化今天的小时数组
      this.setData({
        todayHours: todayHours,
        normalHours: normalHours,
        multiArray: multiArray,
        nowtime:this.data.multiArray[0][0]+this.data.multiArray[1][0]
      })

    },
  
    onShow() {
      this.initHour();
    },

    bindMultiPickerChange(e) {
      this.setData({
        multiIndex: e.detail.value
      })
    },
    bindMultiPickerColumnChange(e) {
      let column = e.detail.column;
      let value = e.detail.value;
      var data = {
        multiArray: this.data.multiArray,
        multiIndex: this.data.multiIndex
      };
      data.multiIndex[column] = value;
      switch (column) {
        case 0: //第一列的变化
          switch (value) {
            case 0:
              data.multiArray[1] = this.data.todayHours; //切换到今天时间数组
              break;
            case 1:
              data.multiArray[1] = this.data.normalHours;
              break;
            case 2:
              data.multiArray[1] = this.data.normalHours;
              break;
          }
          break;
        case 1:
          console.log('multiIndex', data.multiIndex);
          break;
      }
      this.setData(data);
      const multiIndex1 = this.data.multiIndex[0]
      const multiIndex2 = this.data.multiIndex[1]

      this.setData({
        nowtime:this.data.multiArray[0][multiIndex1]+this.data.multiArray[1][multiIndex2]
      })

    },
    testConcat(start = 0) {
      var arrayHours = [];
      for (let i = start; i < 24; i++) {
        if (i < 10) {
          var hourStr = `${i}点`;
        } else {
          var hourStr = `${i}点`;
        }
        arrayHours.push(hourStr);
      }
      return arrayHours;
    },
   
    // 快车跳转添加终点页面
    addEndadr(){
      const token = wx.getStorageSync('token');
      if(token == '' || token == undefined){
        wx.showToast({
          title: '请先登录',
          icon:'none',
        });
        setTimeout(function(){
          wx.redirectTo({
            url: '../loginPage/login',
          })
        },2000)
      }else{
        wx.redirectTo({
          url: '../addEndaddress/add',
        })
      }
    },

    // 换乘车人跳转
    intochangePerson(){
        wx.redirectTo({
          url: '../changePerson/person',
        })
    },
    // 返回
    intoIndex(){
      this.data.isdest = false;
      wx.removeStorageSync("destAddress")
      this.setData({
        isdest: this.data.isdest,
        polyline:[]
      })
    },
    // 呼叫快车
    callcar(){
      const usertel = wx.getStorageSync('usertel')
      if (usertel == '' || usertel == undefined){
           wx.showToast({
             title: '您还未手机号绑定',
             icon:'none',
           });
           setTimeout(function(){
             wx.redirectTo({
               url: '../phonePage/phone',
             })
           },2000)
           return
      }

       wx.setStorageSync('money', this.data.price)
       wx.request({
         url: app.host+'api/callCar/?token='+wx.getStorageSync('token'),
         data:{
            starttime:this.data.nowtime,
            distance:this.data.distance,
            startAddress:this.data.startAddress,
            endAddress:this.data.destAddress,
            token:wx.getStorageSync('token'),
            price:this.data.price,
            ordertype:1,
            passengerName:this.data.passengerName,
            passengertel:this.data.passengertel
         },
         success:res=>{
             console.log(res);
             if(res.data.id == 2){
              wx.showToast({
                title: res.data.msg,
                icon:'none'
              })
              setTimeout(() => {
                wx.redirectTo({
                  url: '../myOrder/myOrder',
                })
              }, 2000);
            }
             if(res.data.id == 1){
                wx.redirectTo({
                  url: '../waitCar/wait',
                })
                wx.removeStorageSync("destAddress");
                wx.setStorageSync('longitude', this.data.startlongitude)
                wx.setStorageSync('latitude', this.data.startlatitude)
                wx.setStorageSync('polyline', this.data.polyline)
                wx.setStorageSync('orderId', res.data.datas)
             }
             
             else{
                wx.showToast({
                  title: res.data.msg,
                  icon:'none'
                })
                setTimeout(function(){
                  wx.redirectTo({
                    url: '../loginPage/login',
                  })
                },2000)
             }
         }
       })
    },
    
    // 顺风车角色点击
    optionRole(e){
       let currentIndex = e.currentTarget.dataset.current
       this.setData({
        currentHitch:currentIndex,
       })
    },

    //  顺风车乘车人数picker
    changePassengerNum(e){
      this.setData({
        passengerNumIndex:e.detail.value
      })
      this.setData({
        hitchOptNum:this.data.passengerNumList[this.data.passengerNumIndex]
      })
      
    },
    
    //  顺风车时间picker
    hitchFirPickerChange(e) {
      this.setData({
        hitchIndex: e.detail.value
      })
      var index1 = this.data.hitchIndex[0]
      var index2 = this.data.hitchIndex[1]
      var index3 = this.data.hitchIndex[2]
      this.setData({
        firstHitchTime:this.data.hitchArray[0][index1]+this.data.hitchArray[1][index2]+this.data.hitchArray[2][index3]
      })
     
    },
    
    hitchLastPickerChange(e) {
      this.setData({
        hitchIndex: e.detail.value
      })
      var index1 = this.data.hitchIndex[0]
      var index2 = this.data.hitchIndex[1]
      var index3 = this.data.hitchIndex[2]
      this.setData({
        lastHitchTime:this.data.hitchArray[0][index1]+this.data.hitchArray[1][index2]+this.data.hitchArray[2][index3]
      })
     
    },
    // 顺风车价格
    countHitchPrice(){
      let km = (this.data.distance/1000).toFixed(1)
      if(km<3){
        this.data.hitchPrice = 10
      }else{
        this.data.hitchPrice = ((km-3)*5+10).toFixed(2)
      }
      this.setData({
        showHitchPrice:'预计'+this.data.hitchPrice+'元'+'前往发布',
        hitchPrice:this.data.hitchPrice
      })
      

    },
    // 呼叫顺风车
    bookHitch(){
      var destAddress = this.data.destAddress;
      var hitchOptNum = this.data.hitchOptNum;
      var firstHitchTime = this.data.firstHitchTime;
      var lastHitchTime = this.data.lastHitchTime;
      var hitchTime = firstHitchTime+lastHitchTime
      if(destAddress == ""){
         wx.showToast({
           title: '还未选择终点！',
           icon:"none"
         })
      }else if(hitchOptNum == ''){
        wx.showToast({
          title: '还未选择乘车人数！',
          icon:"none"
        })
      }else if(firstHitchTime == ''){
        wx.showToast({
          title: '还未选择最早出发时间！',
          icon:"none"
        })
      }else if(lastHitchTime == ''){
        wx.showToast({
          title: '还未选择最晚出发时间！',
          icon:"none"
        })
      }else{
        this.countHitchPrice();
        const usertel = wx.getStorageSync('usertel')
        if (usertel == '' || usertel == undefined){
          wx.showToast({
            title: '您还未手机号绑定',
            icon:'none',
          });
          setTimeout(function(){
            wx.redirectTo({
              url: '../phonePage/phone',
            })
          },2000)
          return
        }
         wx.request({
           url: app.host+'api/callHitch/?token='+wx.getStorageSync('token'),
           data:{
                destAddress:destAddress,
                hitchOptNum:hitchOptNum,
                hitchTime:hitchTime,
                startAddress:this.data.startAddress,
                ordertype:3,
                price:this.data.hitchPrice,
                distance:this.data.distance,
           },
           success:res=>{
             if(res.data.id == 1){
              wx.removeStorageSync("destAddress");
              wx.setStorageSync('longitude', this.data.startlongitude)
              wx.setStorageSync('latitude', this.data.startlatitude)
              wx.setStorageSync('polyline', this.data.polyline)
              wx.setStorageSync('orderId', res.data.datas)
             }
             else{
              wx.showToast({
                title: res.data.msg,
                icon:'none'
              })
              setTimeout(function(){
                wx.redirectTo({
                  url: '../loginPage/login',
                })
              },2000)
           }
           }
         })
      }

    }
    
})
