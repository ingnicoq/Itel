from django.db import models

# Create your models here.


class isdbt(models.Model):
    nombre = models.CharField(max_length=50)
    ip = models.CharField(max_length=20, null=False)
    BR_min = models.FloatField(default=0.5)
    canal_id = models.CharField(max_length=10, null=False)
    estado = models.IntegerField(max_length=11)
    
    def __str__(self):
        return self.name


class megafax(models.Model):
    #nombre_isdbt = models.ForeignKey(isdbt, on_delete=models.CASCADE) Clave foranea enlazada a la primary key de la tabla isdbt , si se borra la clave foranea se borran en cascada todos los datos relacionados
    nombre = models.CharField(max_length=50)
    ip = models.CharField(max_length=20, null=False)
    BR_min = models.FloatField(default=0.5)
    canal_id = models.CharField(max_length=10, null=False)
    estado = models.IntegerField(max_length=11)
    
    def __str__(self):
        return self.name
    

class log(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    min = models.IntegerField()
    sec = models.IntegerField()
    log = models.TextField(max_length=500)


    def __str__(self):
        return self.name