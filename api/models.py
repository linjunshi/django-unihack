
from django.db import models

from rest_framework import serializers


class CarToken (models.Model):
    class Meta:
        unique_together = (('carnum', 'token'))
    
    carnum = models.CharField(max_length=50)
    token = models.CharField(max_length=50)


class CarPark (models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    num = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    address = models.CharField(max_length=50)
    imageurl = models.CharField(max_length=50)

    def __str__(self):
        return '{"id":"%s", "title":"%s"}' % (self.id, self.title)


# Create your models here.
class ParkingTransaction (models.Model):
    id = models.AutoField(primary_key=True)
    parkingLotID = models.CharField(max_length=50)
    carnum = models.CharField(max_length=50)
    timeStartParking = models.DateTimeField()
    timeEndParking = models.DateTimeField(null=True, blank=True)
    parkingLength = models.IntegerField(default=0)
    paid = models.IntegerField(default=0)

    def __str__(self):
        return '{"carnum":"%s", "start":"%s", "end":"%s"}' % (self.carnum, self.timeStartParking, self.timeEndParking)


class CarParkSerializer (serializers.ModelSerializer):
    class Meta:
        model = CarPark
        fields = '__all__'

class TransactionSerializer (serializers.ModelSerializer):
    class Meta:
        model = ParkingTransaction
        fields = '__all__'

 