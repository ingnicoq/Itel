from django.db import models

# Create your models here.


class isdbt(models.Model):
    nombre = models.CharField(max_length=50)
    ip= models.CharField(max_length=20, null=False)
    BR_min = models.FloatField(default=0.5)
    canal_id = models.CharField(max_length=10, null=False)
    estado = models.IntegerField(max_length=11)
    
    def __str__(self):
        return self.name


class megafax(models.Model):
    nombre = models.CharField(max_length=50)
    ip= models.CharField(max_length=20, null=False)
    BR_min = models.FloatField(default=0.5)
    canal_id = models.CharField(max_length=10, null=False)
    estado = models.IntegerField(max_length=11)
    
    def __str__(self):
        return self.name
