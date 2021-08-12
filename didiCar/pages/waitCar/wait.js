// pages/waitCar/wait.js
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    pageToHeight:app.globalData.pageToHeight,
    paddingTopNum:app.globalData.paddingTopNum,
    progress_txt: '已等待',  
    count:0, // 设置 计数器 初始为0
    countTimer: null ,// 设置 定时器 初始为null
    showtime:'0:00'
  },
  cancel(){
    wx.removeStorageSync("destAddress");
    wx.request({
      url: app.host+'api/cancelOrder/?token='+wx.getStorageSync('token'),
      data:{
        orderId:wx.getStorageSync('orderId')
      },
      success:res=>{
        clearInterval(this.countTimer);
        wx.showToast({
          title: '订单已取消',
          icon: "none",
        })
        setTimeout(() => {
          wx.redirectTo({
            url: '/pages/index/index',
          })
        }, 1000);
        wx.removeStorageSync('orderId')    
      }
    })
   
    
  },
  onReady() {
    this.drawProgressbg();
    // this.drawCircle(2) 
    this.countInterval()
  },
  // 圆环
  drawProgressbg(){
    // 使用 wx.createContext 获取绘图上下文 context
    var ctx = wx.createCanvasContext('canvasProgressbg',this)
    ctx.setLineWidth(4);// 设置圆环的宽度
    ctx.setStrokeStyle('#20183b'); // 设置圆环的颜色
    ctx.setLineCap('round') // 设置圆环端点的形状
    ctx.beginPath();//开始一个新的路径
    ctx.arc(110, 110, 100, 0, 2 * Math.PI, false);
    //设置一个原点(110,110)，半径为100的圆的路径到当前路径
    ctx.stroke();//对当前路径进行描边
    ctx.draw();
  },
  // 动态圆环
  drawCircle(step){  
    var context = wx.createCanvasContext('canvasProgress',this);
      // 设置渐变
      var gradient = context.createLinearGradient(200, 100, 100, 200);
      gradient.addColorStop("0", "#2661DD");
      gradient.addColorStop("0.5", "#40ED94");
      gradient.addColorStop("1.0", "#5956CC");
      
      context.setLineWidth(10);
      context.setStrokeStyle(gradient);
      context.setLineCap('round')
      context.beginPath(); 
      // 参数step 为绘制的圆环周长，从0到2为一周 。 -Math.PI / 2 将起始角设在12点钟位置 ，结束角 通过改变 step 的值确定
      context.arc(110, 110, 100, -Math.PI / 2, step * Math.PI - Math.PI / 2, false);
      context.stroke(); 
      context.draw() 
  },

  countInterval() {
    // 设置倒计时 定时器 每100毫秒执行一次，计数器count+1 ,耗时6秒绘一圈
    this.countTimer = setInterval(() => {
         this.drawCircle(this.data.count / (60/2))
         this.data.count++;
         if((this.data.count%60)<10){
             this.data.showtime = Math.floor(this.data.count/60)+':'+0+(this.data.count%60)
         }else{
             this.data.showtime = Math.floor(this.data.count/60)+':'+(this.data.count%60)
         }
         this.setData({
             count:this.data.count,
             showtime:this.data.showtime
         })
         wx.request({
           url: app.host+'api/checkOrderstate/?token='+wx.getStorageSync('token'),
           data:{
               orderId:wx.getStorageSync('orderId')
           },
           success:res=>{
              if(res.data.id == 1){
                clearInterval(this.countTimer);
                this.setData({
                    progress_txt:'司机已接单'
                })
                setTimeout(function(){
                  wx.redirectTo({
                    url: '../waitAccept/waitAccept',
                  })
                },1000)
                wx.setStorageSync('driverInfos', res.data.data1)
              }
           }
         })
    },1000)
  },




  

  


  

})