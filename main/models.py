# main/models.py
from django.db import models
class personal_info(models.Model):
    fullname = models.CharField()
    email = models.CharField()
    phone= models.CharField()
    password= models.CharField()
    businessname= models.CharField()
    date=models.CharField()
    img_tax=models.CharField(null=True)
    img_liability=models.CharField(null=True)
    img_workman=models.CharField(null=True)
    status=models.CharField(default='Pending')
    def __str__(self):
        return self.email
class location(models.Model):
    email = models.CharField()
    city=models.CharField()
    area=models.CharField()
    def __str__(self):
        return self.email
class services(models.Model):
    email = models.CharField()
    services=models.JSONField(default=list)
    def __str__(self):
        return self.email
class preferences(models.Model):
    email = models.CharField()
    preferences=models.JSONField(default=list)
    def __str__(self):
        return self.email

