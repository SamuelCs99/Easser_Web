from django.db import models

# Create your models here.
class series(models.Model):
    id_serie = models.AutoField(primary_key=True)
    serie = models.CharField(max_length=75)
    url = models.URLField()