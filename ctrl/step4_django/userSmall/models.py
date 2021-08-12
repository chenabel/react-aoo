from django.db import models

# Create your models here.
class HistoryPassenge(models.Model):
    historypassenge_id=models.BigAutoField(primary_key=True)
    user_id=models.IntegerField(default=0)
    historypassenge_name=models.CharField(max_length=50,null = True)
    historypassenge_tel=models.CharField(max_length=11,null = True)

class UserInfo(models.Model):
    user_id=models.BigAutoField(primary_key=True)
    user_gh_openid = models.CharField(max_length=50, null=True)
    user_mini_openid = models.CharField(max_length=50, null=True)
    user_nickname=models.CharField(max_length=50,null = True)
    user_sex = models.CharField(max_length=1, null=True)
    user_province = models.CharField(max_length=20, null=True)
    user_city = models.CharField(max_length=20, null=True)
    user_country = models.CharField(max_length=20, null=True)
    user_headimgurl = models.CharField(max_length=255, null=True)
    user_tel = models.CharField(max_length=11, null=True)
    user_registtime=models.DateTimeField(null = True)
    user_money=models.FloatField(default=0)
    user_state = models.IntegerField(default=0)

class OrderInfo(models.Model):
    order_id=models.BigAutoField(primary_key=True)
    user_id=models.IntegerField(default=0)
    driver_id=models.IntegerField(default=0)
    order_startadd=models.CharField(max_length=50, null=True)
    order_destadd=models.CharField(max_length=50, null=True)
    order_distance=models.IntegerField(null=True)
    order_price=models.FloatField(null=True)
    order_pretime =models.CharField(max_length=50, null=True)
    order_starttime=models.DateTimeField(null = True)
    order_desttime=models.DateTimeField(null = True)
    order_passenger=models.CharField(max_length=50, null=True)
    order_tel=models.CharField(max_length=11, null=True)
    order_state=models.IntegerField(default=0)
    order_type=models.IntegerField(default=0)

class Comments(models.Model):
    comments_id=models.BigAutoField(primary_key=True)
    order_id=models.IntegerField(default=0)
    comments_content=models.CharField(max_length=255, null=True)
    comments_level=models.FloatField(default=0)
    comments_time=models.DateTimeField(null=True)


