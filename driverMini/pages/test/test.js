// pages/upload/upload.js
Page({
  data:{
    headHeight:(wx.getSystemInfoSync().statusBarHeight+7)*2 + 70,
    socketOpen:false,
    socketMsgQueue:[]
  },
  onShow(){
  
    wx.connectSocket({
      url: 'ws://127.0.0.1:8000/',
      header: {
        "content-type":'application/json'
      },
      method: 'post',
      success(){
        console.log("连接成功！")
      },
      fail(){
        console.log('连接失败')
      }
    })
    wx.onSocketOpen((result) => {
      this.setData({
        socketOpen:true
      })
      for (let i = 0; i < this.data.socketMsgQueue.length; i++){
        sendSocketMessage(this.data.socketMsgQueue[i])
      }
      this.data.socketMsgQueue = []
    })
  },
  sendSocketMessage(msg) {
    console.log(msg)
    if (this.data.socketOpen) {
      wx.sendSocketMessage({
        data:JSON.stringify(msg)
      })
    }
  },
  sendSocket(e){
    this.sendSocketMessage(123)
  }
})
　　