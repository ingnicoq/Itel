from django.db import models

# Create your models here.


class BR (models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    min = models.IntegerField()
    sec = models.IntegerField()
    canal_id = models.CharField(max_length=30)
    BR = models.IntegerField()
    
    def __str__(self):
        return self.name