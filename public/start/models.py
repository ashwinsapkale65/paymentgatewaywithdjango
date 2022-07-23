from pyexpat import model
from statistics import mode
from django.db import models
from django.forms import DateField


class studentpaymentremaining(models.Model):
    name  =  models.CharField(max_length=122)
    city = models.CharField(max_length=122)
    number = models.CharField(max_length=122)
    date = models.DateField()


    def __str__(self):
        return self.name

class studentpaymentsdone(models.Model):
        name  =  models.CharField(max_length=122)
        city = models.CharField(max_length=122)
        number = models.CharField(max_length=122)
        paymentstatus = models.CharField(max_length=122)
        paymentid = models.CharField(max_length=122)
        orderid = models.CharField(max_length=122)
        signature = models.CharField(max_length=122)
        date = models.DateField()
        time = models.TimeField()

        def __str__(self):
             return self.name




    






