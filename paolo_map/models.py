from django.contrib.gis.db import models


class Marker(models.Model):
    size = models.IntegerField()
    location = models.PointField()

    class Meta:
        db_table = 'marker'