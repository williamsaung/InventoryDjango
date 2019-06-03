from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import ListView
# Create your models here.

class Inventory(models.Model):
    name= models.CharField(max_length=256)
    serial_number = models.CharField(max_length=256)
    price = models.IntegerField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('inventory_tracker:detail',kwargs={'pk':self.pk})






