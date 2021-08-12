const app = getApp()
Page({
  data: {
    headHeight:(wx.getSystemInfoSync().statusBarHeight+7)*2 + 70,
    image1:"",
    image2:"",
    image3:"",
    imageList:[],
    fullImg:false, // 如果有3张图就 不显示上传的图片了
    array: ['男','女'],
    placeholder: '男', 
    openid:"", // 微信给的用户openid
    carNum:"", // 车牌
    name:"", // 姓名
    driverId:"", // 身份证
    sex:"", // 司机性别
    color:'', // 汽车颜色
    brand:'', // 汽车品牌
    disabel:true, // 点击提交信息后就不让点击了
  },

  onShow(){
    wx.getStorageSync('openid')
    this.setData({
      openid:wx.getStorageSync('openid')
    })
  },

  chooseImage() {
    var that = this
    wx.chooseImage({
      count: 1,
      success(res){
        var temp = that.data.imageList
        var name = ''
        temp.push(res.tempFilePaths[0])
        if(that.data.image1 == ''){
          that.setData({
            image1:res.tempFilePaths[0],
            imageList:temp
          })
          name = "身份证正面"
        }else if(that.data.image2 == ''){
          that.setData({
            image2:res.tempFilePaths[0],
            imageList:temp
          })
          name = "身份证反面"
        }else if(that.data.image3 == ''){
          that.setData({
            image3:res.tempFilePaths[0],
            imageList:temp
          })
          name = "驾驶证照片"
        }
        wx.uploadFile({
          url: app.globalData.host + 'api/driver/idPhoto/',
          filePath: res.tempFilePaths[0],
          name: 'file',
          formData: {
            token: that.data.openid,
            type:name
          },
          success() {
            if(that.data.image1 != '' && that.data.image2 != '' && that.data.image3 != ''){
              that.setData({
                fullImg:'true'
              })
            }
          }, 
          fail: function (err) {
            console.log(err)
          }
        });
      }
    })
  },

  previewImage(e){
    wx.previewImage({
      current:e.currentTarget.dataset.src,   //当前图片地址
      urls:[e.currentTarget.dataset.src]
    })
  },

  deleteImg(e){
    this.data.imageList.splice(this.data.imageList.indexOf(e.target.dataset.index),1)
    if(this.data.imageList.length != 3)this.setData({fullImg:false})
    if(this.data.image1 == e.target.dataset.index){
      this.setData({
        image1:''
      })
    }else if(this.data.image2 == e.target.dataset.index){
      this.setData({
        image2:''
      })
    }else{
      this.setData({
        image3:''
      })
    }
  },

  bindPickerChange(e) {
    if(e.detail.value == 1){
      this.setData({
        placeholder: '女'
      })
    }
  },

  submitData(){
    var that = this
    if(this.data.disabel == false)return
    if(this.data.name != ''&& this.data.carNum != '' && this.data.driverId != '' && this.data.imageList.length == 3 && this.data.color != '' && this.data.brand != ''){
      wx.request({
        url: app.globalData.host + 'api/driver/submitData/',
        data:{
          driverTel:app.globalData.driverTel,
          name:this.data.name,
          carNum:this.data.carNum,
          driverId:this.data.driverId,
          idPhotoUp:this.data.openid + '身份证正面',
          idPhotoDown:this.data.openid + '身份证反面',
          carPhoto:this.data.openid + '驾驶证照片',
          color:this.data.color, 
          brand:this.data.brand,
          openid:this.data.openid,
          sex:this.data.placeholder
        },
        method:'post',
        success(res){
          wx.showToast({
            title: res.data.title,
            icon: res.data.type,
            duration: 1500
          })
          that.setData({
            disabel:false
          })
          
        }
      })
    }else if(this.data.name == ''){
      wx.showToast({
        title: '姓名不能为空!',
        icon:'error'
      })
      return
    }else if(this.data.carNum == ''){
      wx.showToast({
        title: '车牌不能为空!',
        icon:'error'
      })
      return
    }else if(this.data.driverId == ''){
      wx.showToast({
        title: '身份证不能为空！',
        icon:'error'
      })
      return
    }else if(this.data.color == ''){
      wx.showToast({
        title: '汽车颜色不能为空',
        icon:'error'
      })
    }else if(this.data.brand == ''){
      wx.showToast({
        title: '汽车品牌不能为空',
        icon:'error'
      })
    } else if(this.data.imageList.length != 3){
      wx.showToast({
        title: '请上传相关照片',
        icon:'error'
      })
    }
  },

  inputData(e){
    var key = e.currentTarget.dataset.driverdata
    if(key == "carNum"){
      this.setData({
        carNum:e.detail.value
      })
    }else if(key == "name"){
      this.setData({
        name:e.detail.value
      })
    }else if(key == "driverId"){
      this.setData({
        driverId:e.detail.value
      })
    }else if(key == 'color'){
      this.setData({
        color:e.detail.value
      })
    }else if(key == 'brand'){
      this.setData({
        brand:e.detail.value
      }) 
    }
  }
})