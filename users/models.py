from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core import serializers
from datetime import date
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # stu_id = models.AutoField(primary_key=True)
    Username=models.CharField(max_length=50,default="")
    UserFirstName=models.CharField(max_length=50,default="")
    UserLastName=models.CharField(max_length=50,default="")
    ProfileImage = models.ImageField(default="default.jpg",upload_to='app/images')
    Gender=models.CharField(max_length=10,default="male")
    UserEmail=models.EmailField(max_length=254,default="")
    Hobbies=models.CharField(max_length=200,default="Cricket")
    Ressidence=models.CharField(max_length=2000,default="Dikshanti app.")
    date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.UserFirstName+" "+self.UserLastName+" Profile"
    
class Incident(models.Model):
    id = models.AutoField(primary_key=True)
    location=models.CharField(max_length=200,default="")
    description=models.CharField(max_length=2000,default="")
    # dateTimeOfIncident=models.DateTimeField(blank=True,null=True)
    incident_date=models.DateField(null=True)
    incident_time=models.TimeField(null=True)
    incident_location=models.CharField(max_length=2000,default="")
    severity=models.CharField(max_length=200,default="")
    cause=models.CharField(max_length=2000,default="")
    actions=models.CharField(max_length=2000,default="")
    type_env=models.BooleanField(default=False)
    type_injury=models.BooleanField(default=False)
    type_property=models.BooleanField(default=False)
    type_vehicle=models.BooleanField(default=False)
    submitted=models.BooleanField(default=False)
    reported_by=models.ForeignKey(User, on_delete=models.CASCADE)
    

