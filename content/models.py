from datetime import date
from django.db import models

# Create your models here.
class Movie(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=255, blank=True)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to = 'thumbnails', blank=True, null=True)
    video_480p = models.CharField(max_length=255, blank=True, null=True)
    video_720p = models.CharField(max_length=255, blank=True, null=True)
    
    
    def __str__(self):
        return self.title