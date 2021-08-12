from django.db import models

# Create your models here.
class CarRentalInfo(models.Model):
    car_id=models.BigAutoField(primary_key=True)
    car_image=models.CharField(max_length=255, null=True)
    car_brand=models.CharField(max_length=10, null=True)
    car_color=models.CharField(max_length=10, null=True)
    car_type=models.CharField(max_length=10, null=True)
    car_rent=models.IntegerField(null=True)
    car_inventory=models.IntegerField(null=True)

class EmployeeInfo(models.Model):
    employee_id=models.BigAutoField(primary_key=True)
    role_id=models.IntegerField(null=True)
    employee_gh_openid = models.CharField(max_length=50, null=True)
    employee_mini_openid = models.CharField(max_length=50, null=True)
    employee_pwd=models.CharField(max_length=50, null=True)
    employee_nickname=models.CharField(max_length=50,null = True)
    employee_name=models.CharField(max_length=10,null = True)
    employee_state=models.IntegerField(null=True)
    employee_tel=models.CharField(max_length=11,null=True)
    employee_registtime=models.DateTimeField(null = True)

class Role(models.Model):
    role_id=models.BigAutoField(primary_key=True)
    role_name=models.CharField(max_length=50, null=True)
    role_describe=models.CharField(max_length=255, null=True)

class Menu(models.Model):
    menu_id=models.BigAutoField(primary_key=True)
    menu_name=models.CharField(max_length=50, null=True)
    role_id=models.IntegerField(null=True)
    menu_url = models.CharField(max_length=50, null=True)

class StateData(models.Model):
    state_id=models.BigAutoField(primary_key=True)
    state_type=models.CharField(max_length=50, null=True)
    state_name=models.CharField(max_length=50, null=True)

class News(models.Model):
    id=models.BigAutoField(primary_key=True)
    news_id=models.IntegerField(null=True)
    news_lang=models.CharField(max_length=50, null=True)
    news_title=models.CharField(max_length=1000, null=True)
    news_content=models.CharField(max_length=1000, null=True)
    news_time=models.DateTimeField(null = True)
    news_img = models.CharField(max_length=255, null=True)

class Province(models.Model):
    province_id=models.BigAutoField(primary_key=True)
    province_name=models.CharField(max_length=50, null=True)

class City(models.Model):
    city_id=models.BigAutoField(primary_key=True)
    city_name=models.CharField(max_length=50, null=True)
    city_spell=models.CharField(max_length=255, null=True)
    city_firstletter=models.CharField(max_length=10, null=True)
    city_smallprice=models.IntegerField(null=True)
    city_bigprice=models.IntegerField(null=True)
    city_note=models.CharField(max_length=255, null=True)
    province_id = models.IntegerField(default=0)

class Advertise(models.Model):
    advertise_id=models.BigAutoField(primary_key=True)
    advertise_image=models.CharField(max_length=255, null=True)
    advertise_url = models.CharField(max_length=255, null=True)
    advertise_starttime=models.DateTimeField(null = True)
    advertise_desttime = models.DateTimeField(null=True)
    advertise_state=models.IntegerField(null=True)

class Service(models.Model):
    service_id=models.BigAutoField(primary_key=True)
    service_site= models.CharField(max_length=255, null=True)
    service_img=models.CharField(max_length=255, null=True)
    service_site_info=models.CharField(max_length=255, null=True)
    province_id=models.IntegerField(null=True)