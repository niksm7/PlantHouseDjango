from django.db import models
from accounts.models import Account
# Create your models here.

class Plant(models.Model):
    plantName = models.CharField(max_length=30)
    plantPrice = models.IntegerField()
    plantImage = models.ImageField(upload_to='nursery/images',default='')
    plantDesc = models.TextField()
    plantNursery = models.CharField(max_length=50,default='',blank=True,null=True)

    def __str__(self):
        return self.plantName

#seperate models for all the nurseries

class Nursery(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name