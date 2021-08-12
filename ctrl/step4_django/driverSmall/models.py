from django.db import models

# Create your models here.
class DriverInfo(models.Model):
    driver_id=models.BigAutoField(primary_key=True)
    driver_gh_openid = models.CharField(max_length=50, null=True)
    driver_mini_openid = models.CharField(max_length=50, null=True)
    driver_name=models.CharField(max_length=11, null=True)
    driver_tel=models.CharField(max_length=11, null=True)
    driver_havecar=models.IntegerField(null=True)
    driver_city_name=models.CharField(max_length=20, null=True)
    driver_license=models.CharField(max_length=255, null=True)
    driver_plate=models.CharField(max_length=10, null=True)
    driver_idcard=models.CharField(max_length=20, null=True)
    driver_idcard_up = models.CharField(max_length=255, null=True)
    driver_idcard_down = models.CharField(max_length=255, null=True)
    driver_type=models.IntegerField(null=True)
    driver_state=models.IntegerField(null=True)
    driver_registtime=models.DateTimeField(null = True)
    driver_carcolor=models.CharField(max_length=10, null=True)
    driver_carbrand=models.CharField(max_length=10, null=True)
    driver_cartype=models.CharField(max_length=10, null=True)
    driver_money=models.IntegerField(default=0)