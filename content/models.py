from datetime import date
from django.db import models

class Category(models.Model):
    CATEGORIES = [
        ('Romance', 'Romance'),
        ('Drama', 'Drama'),
        ('New', 'New'),
        ('Documentary', 'Documentary'),
    ]
    name = models.CharField(max_length=30, choices=CATEGORIES)

    def __str__(self):
        return self.name

# Create your models here.
class Movie(models.Model):


    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=255, blank=True)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to='thumbnails', blank=True, null=True)
    video_480p = models.CharField(max_length=255, blank=True, null=True)
    video_720p = models.CharField(max_length=255, blank=True, null=True)
    video_1080p = models.CharField(max_length=255, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="movies")

    def __str__(self):
        return self.title

