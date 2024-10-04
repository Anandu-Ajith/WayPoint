from django.db import models

# Create your models here.

from django.db import models


class Destination(models.Model):
    place_name = models.CharField(max_length=100)
    weather = models.CharField(max_length=50)
    location_state = models.CharField(max_length=50, null=True)
    location_district = models.CharField(max_length=50)
    google_map_link = models.URLField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.place_name
