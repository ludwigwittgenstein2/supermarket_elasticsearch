from django.db import models

# Create your models here.

class Monthly(models.Model):
    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1)

class Daily(models.Model):
    month = models.IntegerField()
    day = models.IntegerField()
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    rainfall = models.DecimalField(max_digits=5, decimal_places=1)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
