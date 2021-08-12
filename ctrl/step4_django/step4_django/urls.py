"""step4_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from company.ctrl.advertise import *
from company.ctrl.carrental import *
from company.ctrl.city import *
from company.ctrl.employeeInfo import *
from company.ctrl.indexCtrl import *
from company.ctrl.newsCtrl import *
from company.ctrl.role import *
from driverSmall.ctrl.indexCtrl import *
from step4_django.ctrl.public import *
from userSmall.ctrl.userCtrl import *
from userSmall.ctrl.usersmallOrderinfo import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/initMenu/',initMenu),
    path('api/pubilcAuto/',index),
    path('api/userLogin/', userLogin),
    #林佳颖
    # 发送验证码
    path('api/userSendCode/', sendCode),
    # 确认验证
    path('api/userVerify/', verify),
    # 用户初步呼叫订单
    path('api/callCar/', userOrder),
    #  查看订单状态
    path('api/checkOrderstate/', checkOrderstate),
    # 取消订单
    path('api/cancelOrder/', cancelOrder),
    # 换乘车人
    path('api/addPassenger/', addPassenger),
    #  乘车人渲染
    path('api/checkHispassenger/', checkhistoryPassenger),
    #  订单列表
    path('api/checkMyoder/', getOrderlist),
    # 顺风车订单
    path('api/callHitch/', callHitch),
    # 金额渲染
    path('api/checkMoney/', checkMoney),
    # 充值
    path('api/addMoney/', addMoney),
    # 结束行程
    path('api/overOrder/', overOrder),
    # 支付
    path('api/paymoney/', paymoney),
    # 行程中支付
    path('api/myorderPay/', myorderPay),
    # 提交评价
    path('api/commitCom/',commitCom),


    #陈炳祥
    # 司机端的小程序
    path('api/druver/getsessionKey/', getsessionKey),
    path('api/driver/getCode/', driverGetCode),  # 向用户发送验证码
    path('api/driver/doResgister/', verificationCode),  # 保存司机的电话 是否有车 城市所在地
    path('api/driver/idPhoto/', getDriverPhoto),
    path('api/driver/submitData/', getDriverData),
    path('api/driver/getorder/', getDriverOrder),
    path('api/driver/allOrder/', getDriverAllOrder),  # 订单大厅显示所有订单
    path('api/driver/selectDriverOpenid/', selectDriverOpenid),
    path('api/driver/getOrderInfo/', getOrderInfo),
    path('api/driver/getUser/', changeOrder),
    path('api/driver/getOrderData/', orderPageGetOrder),  # 订单界面获取所有未接单的订单
    path('api/driver/getDriverOrder/', getDriverOverOrder),  # 个人中心统计已完成的订单
    path('api/driver/isDriverOrder/', isDriverOrder),  # 判断这个司机有没有为送达顾客的订单
    path('api/driver/getMyOrder/', getMyOrder),  # get司机所有订单
    path('api/driver/getDriverMoney/', getDriverMoney),  # get司机所有订单
    path('api/driver/getDerverLicense/', getDerverLicense),  # get司机驾照信息
    #方立宇代码
    path('api/Driver/', driver),  # 司机数据
    path('api/driverState/', driverState),  # 审核
    path('api/LockState/', LockState),  # 司机锁定
    path('api/UnlockState/', UnlockState),  # 司机解锁
    path('api/getState/', getState),  # 司机状态
    path('api/getType/', getType),  # 司机类型
    path('api/getMethods/', getMethods),  # 获取菜单
    path('api/DetailId/', DetailId),  # 获取数据id
    path('api/getRole/', getRole),  # 获取角色信息
    path('api/addRole/', addRole),  # 添加角色
    path('api/authority/', authority),  # 权限
    path('api/Roledeletes/', Roledeletes),  # 角色删除
    path('api/getEmployeeInfo/', getEmployeeInfo),  # 获取员工信息
    path('api/Stafflocking/', Stafflocking),  # 员工锁定
    path('api/Staffunlock/', Staffunlock),  # 员工解锁
    path('api/getstaffState/', getstaffState),  # 获取员工状态
    path('api/Staffdelete/', Staffdelete),  # 删除员工
    path('api/emjurisdiction/', emjurisdiction),  # 获取员工权限
    path('api/getroles/', getroles),  # 获取员工权限
    path('api/baocun/', baocun),  # 修改员工权限
    path('api/getOrder/', getOrder),  # 获取订单信息
    path('api/getOrderState/', getOrderState),  # 获取订单状态
    path('api/Addemployees/', Addemployees),  # 添加员工
    path('api/getDriverOrder/', getDriverOrder),  # 获取司机订单
    path('api/getRoleMenu/', getRoleMenu),  # 获取全部菜单
    path('api/baocunMenu/', baocunMenu),  # 修改角色权限
    path('api/staffsave/', staffsave),  # 修改员工信息
    path('api/baochundisplay/', baochundisplay),  # 修改角色信息
    path('api/getorderdetails/', getorderdetails),  # 订单详情
    path('api/login/', login),  # 员工登入
    path('api/getCarrent/', getCarrent),  # 获取车辆信息
    path('api/AddCarrental/', AddCarrental),  # 添加车辆
    path('api/scCarrental/', scCarrental),  # 删除车辆
    path('api/baocunMod/', baocunMod),  # 修改车辆信息
    path('api/getCharge/', getCharge),  # 获取city
    path('api/baocunPrice/', baocunPrice),  # 修改city价钱
    path('api/getUserNum/', getUserNum),  # 获取男女分别的用户数量
    path('api/goodsImg/', goodsImg),  # 上传图片
    path('api/getTurnNum/', getTurnNum),  # 营业额统计
    path('api/getDistance/', getDistance),  # 订单距离统计
    path('api/getRegisterRole/', getRegisterRole),  # 获取角色
    path('api/zhuche/', zhuche),  # 注册
    path('api/getRolexx/', getRolexx),  # 获取登入员工信息
    path('api/Servebaocun/', Servebaocun),  # 添加滴滴服务地点
    path('api/getshen/', getshen),  # 获取省份
    path('api/getServe/', getServe),  # 获取滴滴服务信息
    path('api/del/', dels),  # 删除服务信息
    path('api/baocunxx/', baocunxx),  # 修改服务信息
    #陈静
    path('api/getUserState/',getUserState),#获得用户状态的选项
    path('api/User/',User),#用户信息
    path('api/userOrders/', userOrders),  # 用户订单信息
    path('api/AdvertiseData/',getAdvertiseInfo),#广告数据
    path('api/deleteAdvertise/', deleteAdvertise),#删除广告
    path('api/addAdvertise/',addAdvertise),#增加广告
    path('api/initAddr/', selectProvince),
    path('api/initCity/', selectCity),
    path('api/initNews/', findAllNews),
    path('api/initNewsInfo/', FindNews),
    path('api/initNewsDetails/', initNews),
]
