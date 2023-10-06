from django.db import models

# Create your models here.
class Series(models.Model):
    id_serie = models.AutoField(primary_key=True)
    serie = models.CharField(max_length=75)
    url = models.URLField()

    def __str__(self):
        txt = "{0} ({1})"
        return txt.format(self.serie, self.id_serie )