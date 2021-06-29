from django.db import models

# Create your models here.
class Destination(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    desc=models.TextField()
    price=models.IntegerField()
    offer=models.BooleanField(default=False)
    