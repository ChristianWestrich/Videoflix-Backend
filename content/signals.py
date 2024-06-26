import os
from django.dispatch import receiver
from Videoflix.settings import MEDIA_ROOT
from .models import Movie
from django.db.models.signals import post_save, post_delete

from .tasks import convert_480p, convert_720p


@receiver(post_save, sender=Movie)
def video_post_save(sender, instance, created, **kwargs):
    if created and instance.video_file:
        video_480p_path = convert_480p(instance.video_file.path)
        video_720p_path = convert_720p(instance.video_file.path)
        instance.video_480p = video_480p_path.replace(MEDIA_ROOT, '').replace('\\', '/')
        instance.video_720p = video_720p_path.replace(MEDIA_ROOT, '').replace('\\', '/')
        instance.save()
    else:
        pass


@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
        file_root, file_ext = os.path.splitext(instance.video_file.path)
        converted_480p = f"{file_root}_480p.mp4"
        converted_720p = f"{file_root}_720p.mp4"
        
        if os.path.isfile(converted_480p):
            os.remove(converted_480p)
            
        if os.path.isfile(converted_720p):
            os.remove(converted_720p)
            