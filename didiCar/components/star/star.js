Component({
  properties:{
    key:{
      value: 0,//评分
      type:Number
    }
  },
 
  data: {
    stars: [0, 1, 2, 3, 4],
    normalSrc: '/icons/nullstar.png',
    selectedSrc: '/icons/fullstar.png',
    halfSrc: '/icons/halfstar.png',
    showTap:true//是否可以点击
  },
  methods: {
    
    //点击左边,半颗星
    selectLeft: function (e) {
      var key = e.currentTarget.dataset.key
      if (this.data.key == 0.5 && e.currentTarget.dataset.key == 0.5) {
        //只有一颗星的时候,再次点击,变为0颗
        key = 0;
      }
      this.setData({
        key: key
      })
      this.triggerEvent('comment',{params:this.data.key },{})
    },
    //点击右边,整颗星
    selectRight: function (e) {
      var key = e.currentTarget.dataset.key
      this.setData({
        key: key
      })
      this.triggerEvent('comment',{params: this.data.key},{})
    },
   

  },
  attached: function () {
    if (this.properties.key!=0){
      this.setData({
        showTap: false
      })
    }
  }
})
